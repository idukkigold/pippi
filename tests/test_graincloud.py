from os import path
import random
import shutil
import tempfile
from unittest import TestCase

from pippi.soundbuffer import SoundBuffer
from pippi import dsp, grains

class TestCloud(TestCase):
    def setUp(self):
        self.soundfiles = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.soundfiles)

    def test_unmodulated_graincloud(self):
        sound = SoundBuffer(filename='tests/sounds/guitar1s.wav')
        cloud = grains.Cloud(sound)

        length = random.triangular(1, 4)
        framelength = int(length * sound.samplerate)

        out = cloud.play(length)
        self.assertEqual(len(out), framelength)

        out.write('tests/renders/test_unmodulated_graincloud.wav')

    def test_pulsed_graincloud(self):
        sound = SoundBuffer(filename='tests/sounds/guitar1s.wav')
        out = sound.cloud(10, grainlength=0.06, grid=0.12)
        out.write('tests/renders/test_pulsed_graincloud.wav')

    def test_long_graincloud(self):
        sound = SoundBuffer(filename='examples/sounds/linus.wav')
        length = 90
        grainlength = dsp.wt(dsp.HANN) * 0.08 + 0.01
        grid = dsp.wt(dsp.HANN) * 0.1 + 0.01

        out = sound.cloud(length, 
                grainlength=grainlength,
                grid=grid,
                spread=0.5,
        )

        framelength = int(length * sound.samplerate)
        self.assertEqual(len(out), framelength)

        out.write('tests/renders/test_long_graincloud.wav')

    def test_graincloud_with_length_lfo(self):
        sound = SoundBuffer(filename='tests/sounds/guitar1s.wav')
        grainlength = dsp.wt(dsp.HANN) * 0.1 + 0.01
        length = 10
        framelength = int(length * sound.samplerate)

        out = sound.cloud(length, grainlength=grainlength)

        self.assertEqual(len(out), framelength)

        out.write('tests/renders/test_graincloud_with_length_lfo.wav')

    def test_graincloud_with_speed_lfo(self):
        sound = SoundBuffer(filename='tests/sounds/guitar1s.wav')
        minspeed = random.triangular(0.05, 1)
        maxspeed = minspeed + random.triangular(0.5, 10)
        speed = dsp.wt(dsp.RND) * (maxspeed - minspeed) + minspeed
        cloud = grains.Cloud(sound, grainlength=0.04, speed=speed)

        length = 30
        framelength = int(length * sound.samplerate)

        out = cloud.play(length)
        self.assertEqual(len(out), framelength)

        out.write('tests/renders/test_graincloud_with_speed_lfo.wav')

    def test_graincloud_with_read_lfo(self):
        sound = SoundBuffer(filename='examples/sounds/linus.wav')
        cloud = grains.Cloud(sound, 
                            position=dsp.wt(dsp.HANN) * sound.dur, 
                        )

        length = 30
        framelength = int(length * sound.samplerate)

        out = cloud.play(length)
        self.assertEqual(len(out), framelength)

        out.write('tests/renders/test_graincloud_with_read_lfo.wav')


