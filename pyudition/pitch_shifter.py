#!/usr/bin/python3

class Pitchshifter:
    """pitch shift class:"""

    @property
    def max_frame_length(self):
        """constant"""
        return 8192

    def setup(self, fft_frame_size, sample_rate, osamp):
        """sets up fields"""
        self.fft_frame_size2 = fft_frame_size//2
        self.step_size = fft_frame_size//osamp
        self.freq_per_bin = sample_rate/fft_frame_size
        self.expct = 2*math.pi*self.step_size/fft_frame_size
        self.in_fifo_latency = fft_frame_size - self.step_size
        self.g_rover = self.in_fifo_latency

        self.g_in_fifo = [0 for _ in range(self.max_frame_length)]
        self.g_out_fifo = [0 for _ in range(self.max_frame_length)]
        self.g_fft_worksp = [0 for _ in range(self.max_frame_length*2)]
        self.g_last_phase = [0 for _ in range(self.max_frame_length//2 + 1)]
        self.g_sum_phase = [0 for _ in range(self.max_frame_length//2 + 1)]
        self.g_output_accum = [0 for _ in range(self.max_frame_length*2)]
        self.g_ana_freq = [0 for _ in range(self.max_frame_length)]
        self.g_ana_magn = [0 for _ in range(self.max_frame_length)]

    def shift(self, pitch_shift, fft_frame_size, sample_rate, osamp, indata):
        """shifts data"""
        self.setup(fft_frame_size, sample_rate, osamp)
        outdata = []
        for value in indata:
            self.g_in_fifo[self.g_rover] = value
            outdata.append(self.g_out_fifo[self.g_rover -
                                           self.in_fifo_latency])
            self.g_rover += 1
            if self.g_rover >= fft_frame_size:
                self.g_rover = self.in_fifo_latency
                for k in range(fft_frame_size):
                    window = -0.5*math.cos(2*math.pi*k/fft_frame_size)+0.5
                    self.g_fft_worksp[2*k] = self.g_in_fifo[k] * window
                    self.g_fft_worksp[2*k + 1] = 0
                self.analysis(fft_frame_size, osamp)
                self.processing(fft_frame_size, pitch_shift)
                self.synthesis(fft_frame_size, osamp)
        return outdata

    def analysis(self, fft_frame_size, osamp):
        """analysis"""
        self.smb_fft(self.g_fft_worksp, fft_frame_size, -1)
        for k in range(self.fft_frame_size2 + 1):
            real = self.g_fft_worksp[2*k]
            imag = self.g_fft_worksp[2*k + 1]

            magn = 2*math.sqrt(real*real + imag*imag)
            phase = math.atan2(imag, real)

            tmp = phase - self.g_last_phase[k]
            self.g_last_phase[k] = phase
            tmp -= k*self.expct

            qpd = int(tmp/math.pi)
            if qpd >= 0:
                qpd += qpd & 1
            else:
                qpd -= qpd & 1
            tmp -= math.pi*qpd

            tmp = osamp*tmp/(2*math.pi)

            tmp = k*self.freq_per_bin + tmp*self.freq_per_bin

            self.g_ana_magn[k] = magn
            self.g_ana_freq[k] = tmp

    def processing(self, fft_frame_size, pitch_shift):
        """processing"""
        self.g_syn_magn = [0 for _ in range(fft_frame_size)]
        self.g_syn_freq = [0 for _ in range(fft_frame_size)]
        for k in range(self.fft_frame_size2 + 1):
            index = int(k*pitch_shift)
            if index <= self.fft_frame_size2:
                self.g_syn_magn[index] += self.g_ana_magn[k]
                self.g_syn_freq[index] = self.g_ana_freq[k]*pitch_shift

    def synthesis(self, fft_frame_size, osamp):
        """synthesys"""
        for k in range(self.fft_frame_size2 + 1):
            magn = self.g_syn_magn[k]
            tmp = self.g_syn_freq[k]

            tmp -= k*self.freq_per_bin

            tmp /= self.freq_per_bin

            tmp = 2*math.pi*tmp/osamp

            tmp += k*self.expct

            self.g_sum_phase[k] += tmp
            phase = self.g_sum_phase[k]

            self.g_fft_worksp[2*k] = magn*math.cos(phase)
            self.g_fft_worksp[2*k + 1] = magn*math.sin(phase)

        for k in range(fft_frame_size + 2, 2*fft_frame_size):
            self.g_fft_worksp[k] = 0

        self.smb_fft(self.g_fft_worksp, fft_frame_size, 1)

        for k in range(fft_frame_size):
            window = -0.5*math.cos(2*math.pi*k/fft_frame_size)+0.5
            value = self.g_fft_worksp[2 * k]/(self.fft_frame_size2*osamp)
            self.g_output_accum[k] += 2*window*value
        for k in range(self.step_size):
            self.g_out_fifo[k] = self.g_output_accum[k]

        for k in range(fft_frame_size):
            self.g_output_accum[k] = self.g_output_accum[k + self.step_size]

        for k in range(self.in_fifo_latency):
            self.g_in_fifo[k] = self.g_in_fifo[k + self.step_size]

    def smb_fft(self, fft_buffer, fft_frame_size, sign):
        """fast fourier transform"""
        for i in range(2, 2*fft_frame_size - 2, 2):
            bitm = 2
            j = 0
            while bitm < 2*fft_frame_size:
                if i & bitm == 0:
                    j += 1
                j <<= 1
                bitm <<= 1
            if i < j:
                temp = fft_buffer[i]
                fft_buffer[i] = fft_buffer[j]
                fft_buffer[j] = temp
                temp = fft_buffer[i + 1]
                fft_buffer[i + 1] = fft_buffer[j + 1]
                fft_buffer[j + 1] = temp

        le1 = 2
        border = int(math.log(fft_frame_size)/math.log(2) + 0.5)
        for _ in range(border):
            le1 <<= 1
            le21 = le1 >> 1
            ur1 = 1.0
            ui1 = 0.0
            arg = math.pi / (le21 >> 1)
            wr1 = math.cos(arg)
            wi1 = sign*math.sin(arg)
            for j in range(0, le21, 2):
                for i in range(j, 2*fft_frame_size, le1):
                    tr1 = fft_buffer[i + le21]*ur1 - \
                          fft_buffer[i + le21 + 1]*ui1
                    ti1 = fft_buffer[i + le21]*ui1 + \
                          fft_buffer[i + le21 + 1]*ur1
                    fft_buffer[i + le21] = fft_buffer[i] - tr1
                    fft_buffer[i + le21 + 1] = fft_buffer[i + 1] - ti1
                    fft_buffer[i] += tr1
                    fft_buffer[i + 1] += ti1
                tr1 = ur1*wr1 - ui1*wi1
                ui1 = ur1*wi1 + ui1*wr1
                ur1 = tr1


