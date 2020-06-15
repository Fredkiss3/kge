import unittest
from typing import List

from kge import Animation, Frame, Entity, Vector, DEFAULT_FPS, EasingFunction


class SmoothStart2(EasingFunction):
    def compute(self, t: float):
        return t ** 2


class InvalidEasing(EasingFunction):
    def compute(self, t: float) -> float:
        return t + 2


class AnimTestCase(unittest.TestCase):

    def s_anim(self, frames: List[Frame] = None, loop=False):
        if frames is None:
            frames = [
                Frame(name="hello", duration=.1),
                Frame(name="my friend !", duration=.1),
                Frame(name="How are you ?", position=Vector.Down(), duration=.1),
            ]

        return Animation(
            self.e,
            frames=frames,
            name="test_anim",
            loop=loop
        )

    def setUp(self) -> None:
        self.e = Entity()
        f1 = Frame(name="hello", duration=.1)
        frames = [
            f1,
        ]
        # self.anim = Animation(
        #     self.e,
        #     frames=frames,
        #     name="test_anim",
        #     loop=True
        # )
        # self.smothed_anim = Animation(
        #     self.e,
        #     [
        #         Frame(name="hello", duration=.1),
        #         Frame(name="hello", duration=.5),
        #     ],
        #     name="test_anim",
        #     easing_function=Animation.Lerp
        # )

    def test_sample_stepped_animation(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="kiss", duration=.5)
        f3 = Frame(name="game", duration=.75)
        f4 = Frame(name="Engine", duration=.4)
        frames = [
            f1, f2, f3, f4
        ]
        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=None
        )

        self.assertEqual(len(frames), len(anim.samples))
        self.assertEqual(sum([f.duration for f in frames]), anim.length)
        self.assertIsInstance(anim.samples, dict)
        self.assertEqual(f1, anim.samples[0])
        self.assertEqual(f2, anim.samples[0.1])
        self.assertEqual(f3, anim.samples[0.6])
        self.assertEqual(f4, anim.samples[1.35])

    def test_sample_lerp_animation_duration(self):
        f1 = Frame(position=Vector.Up(), duration=.1)
        f4 = Frame(position=Vector.Down(), duration=.5)
        f6 = Frame(position=Vector.Down(), duration=.25)
        frames = [
            f1, f4, f6
        ]

        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=Animation.Lerp
        )

        self.assertLessEqual(anim.length, sum([f.duration for f in frames]) + .16)
        self.assertGreaterEqual(anim.length, sum([f.duration for f in frames]) - .16)
        self.assertGreaterEqual(len(anim.samples), int(sum([f.duration for f in frames[:-1]]) * DEFAULT_FPS) - 3)
        # self.assertLessEqual(len(anim.frames), int(sum([f.duration for f in frames[:-1]]) * DEFAULT_FPS) + 3)

        for k, f in anim.samples.items():
            self.assertLessEqual(f["position"], Vector.Down())
            if k > .6:
                self.assertAlmostEqual(.61, k, 1)

    def test_lerp_animation_in_range(self):
        f1 = Frame(position=Vector.Up(), duration=.1)
        f4 = Frame(position=Vector.Down(), duration=.5)
        # f6 = Frame(position=Vector.Down(), duration=.25)
        frames = [
            f1, f4
        ]

        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=Animation.Lerp
        )

        for f in anim.samples.values():
            self.assertLessEqual(f["position"], Vector.Down())

    def test_lerp_animation_states_distribued_correctly(self):
        f1 = Frame(position=Vector.Up(), duration=.1)
        f4 = Frame(position=Vector.Down(), duration=.5)
        f6 = Frame(position=Vector.Down() * 2, duration=.25)
        frames = [
            f1, f4, f6
        ]

        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=Animation.Lerp
        )

        k = max([k for k in anim.samples])
        last = anim.samples[k]
        self.assertGreater(last["position"], Vector.Down())

    def test_smoothstart_animation_states_distribued_correctly(self):
        f1 = Frame(position=Vector.Up(), duration=.1)
        f4 = Frame(position=Vector.Down(), duration=.5)
        f6 = Frame(position=Vector.Down() * 2, duration=.25)
        frames = [
            f1, f4, f6
        ]

        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=SmoothStart2
        )

        k = max([k for k in anim.samples])
        last = anim.samples[k]
        self.assertGreater(last["position"], Vector.Down())

    def test_invalid_easing_function(self):
        f1 = Frame(position=Vector.Up(), duration=.1)
        f4 = Frame(position=Vector.Down(), duration=.5)
        f6 = Frame(position=Vector.Down() * 2, duration=.25)
        frames = [
            f1, f4, f6
        ]

        with self.assertRaises(ValueError):
            anim = Animation(
                self.e,
                frames=frames,
                name="test_anim",
                easing=InvalidEasing
            )

    def test_single_frame_step_anim(self):
        f1 = Frame(name="hello", duration=.1)
        frames = [
            f1,
        ]
        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=None
        )

        self.assertEqual(len(anim.samples), 1)
        self.assertEqual(anim.length, sum([f.duration for f in frames]))

    def test_single_frame_eased_anim(self):
        f1 = Frame(name="hello", duration=.1)
        frames = [
            f1,
        ]
        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            easing=Animation.Lerp()
        )

        self.assertEqual(len(anim.samples), 1)
        self.assertEqual(anim.length, sum([f.duration for f in frames]))

    def test_stepped_anim_played_correctly(self):
        f1 = Frame(name="hello", duration=.1)
        frames = [
            f1,
        ]
        anim = Animation(
            self.e,
            frames=frames,
            name="test_anim",
            loop=False
        )

        self.assertIsNone(anim.current_frame)
        self.assertEqual(f1, anim.next_frame)
        anim.play()
        self.assertEqual(len(anim.samples), 1)
        self.assertEqual(self.e.name, 'hello')
        self.assertIsNone(anim.next_frame)
        self.assertEqual(f1, anim.current_frame)

    def test_stepped_anim_with_loop_played_correctly(self):
        f1 = Frame(name="hello", duration=.1)
        frames = [
            f1,
        ]
        anim = self.s_anim(frames, loop=True)

        self.assertIsNone(anim.current_frame)
        self.assertEqual(f1, anim.next_frame)
        anim.play()
        self.assertEqual(len(anim.samples), 1)
        self.assertEqual(self.e.name, 'hello')
        self.assertIsNotNone(anim.next_frame)
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f1, anim.next_frame)

    def test_lerp_anim_sampled_correctly_with_vectors(self):
        anim = Animation(
            self.e,
            [
                Frame(position=Vector.Up(), duration=1),
                Frame(position=Vector.Down(), duration=.3),
            ],
            loop=True,
            easing=Animation.Lerp
        )

        anim.play()
        self.assertEqual(Vector.Up(), self.e.position)
        anim.play()
        self.assertLess(self.e.position, Vector.Up())
        self.assertGreater(self.e.position.y, Vector.Down().y)

    def test_lerp_anim_first_frame_duration_changed(self):
        anim = Animation(
            self.e,
            [
                Frame(position=Vector.Up(), duration=1),
                Frame(position=Vector.Down(), duration=.3),
            ],
            loop=True,
            easing=Animation.Lerp
        )

        self.assertEqual(1 / DEFAULT_FPS, anim.samples[0].duration)

    def test_lerp_anim_sampled_correctly_with_int_reversed(self):
        anim = Animation(
            self.e,
            [
                Frame(layer=1, duration=1),
                Frame(layer=-1, duration=.3),
            ],
            loop=True,
            easing=Animation.Lerp
        )

        anim.play()
        anim.play()
        anim.play()
        self.assertLess(self.e.layer, 1)
        self.assertGreater(self.e.layer, -1)

    def test_lerp_anim_sampled_correctly_with_int(self):
        anim = Animation(
            self.e,
            [
                Frame(layer=-1, duration=1),
                Frame(layer=1, duration=.3),
            ],
            loop=True,
            easing=Animation.Lerp
        )

        anim.play()
        anim.play()
        anim.play()
        self.assertLess(self.e.layer, 1)
        self.assertGreater(self.e.layer, -1)

    def test_step_anim_going_forward(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames)
        anim.play()
        self.assertEqual('hello', self.e.name)
        self.assertEqual(Vector.Zero(), self.e.position)
        anim.play()
        self.assertEqual('my friend !', self.e.name)
        self.assertEqual(Vector.Zero(), self.e.position)
        anim.play()
        self.assertEqual(Vector.Down(), self.e.position)
        self.assertEqual('How are you ?', self.e.name)

    def test_step_anim_frames_goind_forward(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames)
        self.assertEqual(3, len(anim.samples))
        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f2, anim.next_frame)
        anim.play()
        self.assertEqual(f2, anim.current_frame)
        self.assertEqual(f3, anim.next_frame)
        anim.play()
        self.assertEqual(f3, anim.current_frame)
        self.assertEqual(None, anim.next_frame)

    def test_step_anim_with_loop_frames_goind_forward(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames, loop=True)
        self.assertEqual(3, len(anim.samples))
        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f2, anim.next_frame)
        anim.play()
        self.assertEqual(f2, anim.current_frame)
        self.assertEqual(f3, anim.next_frame)
        anim.play()
        self.assertEqual(f3, anim.current_frame)
        self.assertEqual(f1, anim.next_frame)
        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f2, anim.next_frame)

    def test_step_anim_paused_correctly(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames)

        anim.play()
        anim.pause()
        self.assertEqual(f1, anim.current_frame)
        self.assertTrue(anim.paused)

        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertTrue(anim.paused)

        anim.unpause()
        anim.play()
        self.assertEqual(f2, anim.current_frame)
        self.assertFalse(anim.paused)


    def test_step_anim_restarted_correctly(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames)
        anim.play()
        anim.play()
        anim.play()
        self.assertTrue(anim.finished)
        anim.restart()
        self.assertFalse(anim.finished)
        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f2, anim.next_frame)

    def test_step_anim_stay_still_after_finished(self):
        f1 = Frame(name="hello", duration=.1)
        f2 = Frame(name="my friend !", duration=.1)
        f3 = Frame(name="How are you ?", position=Vector.Down(), duration=.1)
        frames = [
            f1, f2, f3
        ]

        anim = self.s_anim(frames)
        self.assertEqual(3, len(anim.samples))
        anim.play()
        self.assertEqual(f1, anim.current_frame)
        self.assertEqual(f2, anim.next_frame)
        anim.play()
        self.assertEqual(f2, anim.current_frame)
        self.assertEqual(f3, anim.next_frame)
        anim.play()
        self.assertEqual(f3, anim.current_frame)
        self.assertEqual(None, anim.next_frame)
        self.assertTrue(anim.finished)
        anim.play()
        self.assertEqual(f3, anim.current_frame)
        self.assertEqual(None, anim.next_frame)


if __name__ == '__main__':
    unittest.main()
