import unittest
from typing import Callable, Tuple

import pyglet

from kge import Animator, Animation, Entity, Frame, Vector, C, ANY  # , ALWAYS


class CustomEntity(Entity):
    def __init__(self):
        self._name = "Custom"


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        # print(f"Changing Name to {value}")

class AnimatorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.e = CustomEntity()

    def run_anim(self, anim: Animator, *callbacks: Tuple[Callable, float], end: float = 1, ):
        anim.animate()

        for callback in callbacks:
            if callback is not None:
                pyglet.clock.schedule_once(callback[0], callback[1])

        pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), end)
        pyglet.app.run()

    def anim_c(self, *animations: Animation):
        self.animator = Animator(*animations)
        self.e.addComponent(self.animator)
        return self.animator

    def test_animator_playing_anim(self):
        anim = self.anim_c(
            Animation(
                self.e,
                [
                    Frame(name="Fred", duration=.3),
                    Frame(name="Kiss 3", duration=.3),
                    Frame(name="The Boss", duration=.3),
                ],
                loop=False
            ))

        self.run_anim(anim, end=2)
        self.assertEqual(self.e.name, 'The Boss')

    def test_animator_playing_lerp_anim(self):
        anim = self.anim_c(
            Animation(
                self.e,
                [
                    Frame(position=Vector.Up(), duration=.3),
                    Frame(position=Vector.Down(), duration=.3),
                ],
                loop=False
            ))

        self.run_anim(anim, end=1)
        self.assertEqual(Vector.Down(), self.e.position)

    def test_animator_playing_lerp_anim_and_looping(self):
        an = Animation(
            self.e,
            [
                Frame(position=Vector.Up(), duration=1),
                Frame(position=Vector.Down(), duration=.3),
            ],
            loop=True,
            easing=Animation.Lerp
        )

        animator = self.anim_c(an)

        stop = (lambda dt: animator.pause(), .5)
        self.run_anim(animator, stop, end=3)
        self.assertLessEqual(self.e.position.y, .5)
        self.assertGreaterEqual(self.e.position.y, 0)

    def test_animator_frame_by_frame_loop_working_correctly(self):
        frames = [
            Frame(position=Vector.Up(), duration=1),
            Frame(position=Vector.Zero(), duration=1),
            Frame(position=Vector.Down(), duration=.3),
        ]
        an = Animation(
            self.e,
            frames,
            loop=True,
        )

        animator = self.anim_c(an)

        # First Run
        self.assertEqual(an, animator.next.state)
        self.assertIsNone(an.current_frame)
        self.assertIsNone(animator.current)
        self.assertIsNotNone(animator.next)
        self.assertFalse(animator.pending)

        # Run 3 times
        for i in range(3):
            animator.animate()
            self.assertEqual(an, animator.current.state)
            self.assertEqual(frames[0], an.current_frame)
            self.assertEqual(frames[0], animator.current.state.current_frame)
            self.assertEqual(Vector.Up(), self.e.position)
            self.assertIsNotNone(animator.current)
            self.assertFalse(animator.pending)
            self.assertIsNotNone(animator.next)

            animator.animate()
            self.assertEqual(an, animator.current.state)
            self.assertEqual(frames[1], an.current_frame)
            self.assertEqual(frames[1], animator.current.state.current_frame)
            self.assertEqual(Vector.Zero(), self.e.position)
            self.assertIsNotNone(animator.current)
            self.assertFalse(animator.pending)

            animator.animate()
            self.assertEqual(an, animator.current.state)
            self.assertEqual(frames[-1], an.current_frame)
            self.assertEqual(frames[-1], animator.current.state.current_frame)
            self.assertEqual(Vector.Down(), self.e.position)
            self.assertIsNotNone(animator.current)
            self.assertFalse(an.finished)
            self.assertFalse(animator.pending)

    def test_animator_frame_by_frame_not_loop_working_correctly(self):
        frames = [
            Frame(position=Vector.Up(), duration=1),
            Frame(position=Vector.Zero(), duration=1),
            Frame(position=Vector.Down(), duration=.3),
        ]
        an = Animation(
            self.e,
            frames,
            loop=False,
        )

        animator = self.anim_c(an)

        # Initial state
        self.assertEqual(an, animator.next.state)
        self.assertIsNone(an.current_frame)
        self.assertIsNone(animator.current)
        self.assertIsNotNone(animator.next)
        self.assertFalse(animator.pending)

        # Go to the first frame
        animator.animate()
        self.assertEqual(an, animator.current.state)
        self.assertEqual(frames[0], an.current_frame)
        self.assertEqual(frames[0], animator.current.state.current_frame)
        self.assertEqual(Vector.Up(), self.e.position)
        self.assertIsNotNone(animator.current)
        self.assertFalse(animator.pending)
        self.assertIsNotNone(animator.next)

        # Go to the second frame
        animator.animate()
        self.assertEqual(an, animator.current.state)
        self.assertEqual(frames[1], an.current_frame)
        self.assertEqual(frames[1], animator.current.state.current_frame)
        self.assertEqual(Vector.Zero(), self.e.position)
        self.assertIsNotNone(animator.current)
        self.assertFalse(animator.pending)
        self.assertIsNotNone(animator.next)

        # Go to the third frame
        animator.animate()
        self.assertEqual(an, animator.current.state)
        self.assertEqual(frames[-1], an.current_frame)
        self.assertEqual(frames[-1], animator.current.state.current_frame)
        self.assertEqual(Vector.Down(), self.e.position)
        self.assertIsNotNone(animator.current)
        self.assertTrue(an.finished)
        self.assertTrue(animator.pending)
        self.assertIsNone(animator.next)

        # Try to go forward again, but animator has already finished
        animator.animate()
        self.assertTrue(animator.pending)
        self.assertIsNone(animator.next)
        self.assertIsNotNone(animator.current)
        self.assertEqual(an, animator.current.state)
        self.assertEqual(frames[-1], an.current_frame)
        self.assertEqual(frames[-1], animator.current.state.current_frame)
        self.assertEqual(Vector.Down(), self.e.position)

    def test_animator_frame_by_frame_not_loop_paused_correctly(self):
        frames = [
            Frame(position=Vector.Up(), duration=1),
            Frame(position=Vector.Zero(), duration=1),
            Frame(position=Vector.Down(), duration=.3),
        ]
        an = Animation(
            self.e,
            frames,
            loop=False,
        )

        animator = self.anim_c(an)

        # Pause to the second frame
        animator.animate()
        animator.animate()
        animator.pause()
        self.assertEqual(Vector.Zero(), self.e.position)

        # Test if even if anim is stopped, we cannot go forward
        animator.animate()
        self.assertEqual(Vector.Zero(), self.e.position)
        self.assertTrue(an.paused)

        # Continue
        animator.unpause()
        animator.animate()
        self.assertEqual(Vector.Down(), self.e.position)
        self.assertFalse(an.paused)

    def test_animator_frame_by_frame_with_transitions(self):
        an = Animation(
            self.e,
            [
                Frame(position=Vector.Up(), duration=1),
                Frame(position=Vector.Zero(), duration=1),
                Frame(position=Vector.Down(), duration=.3),
            ],
            loop=False,
        )

        an2 = Animation(
            self.e,
            [
                Frame(position=Vector.Left(), duration=1),
                Frame(position=Vector.Zero(), duration=.71),
                Frame(position=Vector.Right(), duration=.305),
            ],
            loop=False,
        )

        animator = self.anim_c(an, an2)
        animator.add_transition(an, an2)

        self.assertEqual(an, animator.next.state)

        # ============================ First Animation ============================= #
        # First Frame
        animator.animate()
        self.assertEqual(Vector.Up(), self.e.position)
        self.assertEqual(an, animator.next.state)

        # Second Frame
        animator.animate()
        self.assertEqual(Vector.Zero(), self.e.position)
        self.assertEqual(an, animator.next.state)

        # Third Frame
        animator.animate()
        self.assertEqual(Vector.Down(), self.e.position)
        self.assertEqual(an2, animator.next.state)

        # ============================ First Animation ============================= #
        # First Frame
        animator.animate()
        self.assertEqual(Vector.Left(), self.e.position)
        self.assertEqual(an2, animator.next.state)

        # Second Frame
        animator.animate()
        self.assertEqual(Vector.Zero(), self.e.position)
        self.assertEqual(an2, animator.next.state)

        # Third Frame
        animator.animate()
        self.assertEqual(Vector.Right(), self.e.position)
        self.assertIsNone(animator.next)

    def test_animator_frame_by_frame_updating_entity_correctly(self):
        f1 = Frame(name="Fred", duration=.3)
        f2 = Frame(name="Kiss 3", duration=.3)
        f3 = Frame(name="The Boss", duration=.3)
        an = Animation(
            self.e,
            [
                f1, f2, f3
            ]
        )

        anim = self.anim_c(an)

        anim.animate()
        self.assertEqual("Fred", self.e.name)
        anim.animate()
        self.assertEqual("Kiss 3", self.e.name)
        anim.animate()
        self.assertEqual('The Boss', self.e.name)

    def test_animator_and_entity_binded_correctly(self):
        anim = self.anim_c(
            Animation(
                self.e,
                [
                    Frame(name="Fred", duration=.3),
                    Frame(name="Kiss 3", duration=.3),
                    Frame(name="The Boss", duration=.3),
                ]
            ))
        self.assertNotIn('entity', anim.fields)
        self.assertEqual(anim, self.e.getComponent(Animator))
        self.assertEqual(self.e, anim.entity)

    def test_animator_fields_accessed_without_error(self):
        anim = self.anim_c(
            Animation(
                self.e,
                [
                    Frame(name="Fred", duration=.3),
                    Frame(name="Kiss 3", duration=.3),
                    Frame(name="The Boss", duration=.3),
                ]
            ))

        anim['jumping'] = False
        anim['velx'] = Vector.Zero()

        self.assertFalse(anim["jumping"])
        self.assertEqual(anim["velx"], Vector.Zero())
        self.assertNotIn('jumping', anim.__dict__)
        self.assertIn('jumping', anim.fields)
        self.assertIn('current', anim.__dict__)

        anim.set(velx=Vector.Up(), jumping=True)
        self.assertTrue(anim["jumping"])
        self.assertEqual(anim.get('velx'), Vector.Up())
        self.assertNotIn('jumping', anim.__dict__)
        self.assertIn('jumping', anim.fields)

    def test_animator_frame_by_frame_switching_anim_on_condition(self):
        an1 = Animation(
            self.e,
            [
                Frame(name="Fred", duration=.3),
                Frame(name="Kiss 3", duration=.3),
                Frame(name="The Boss", duration=.3),
            ]
        )

        an2 = Animation(
            self.e,
            [
                Frame(name="Hello", duration=.3),
                Frame(name="Kitty", duration=.3),
            ]
        )

        # an3 = Animation(
        #     self.e,
        #     [
        #         Frame(name="Hello", duration=.3),
        #         Frame(name="Unknown", duration=.3),
        #     ]
        # )

        animator = self.anim_c(an1, an2, )
        animator['person'] = 1

        # Setup Transitions
        animator.add_transition(an1, an2, C(person=2), C(person=1))
        # animator.add_transition(ANY, an3, C(person=1), ~C(person=1))
        # animator.add_transition(an3, an1, C(person=1))
        # animator.add_transition(an3, an2, C(person=2))

        for i in range(3):
            # ================= First Animation ===================== #
            animator.animate()  # first frame
            animator.animate()  # second frame
            animator.animate()  # third frame
            animator.animate()  # first again
            self.assertEqual(an1, animator.current.state)

            # ================ Second Animation ===================== #
            animator.set(person=2)
            self.assertEqual(an2, animator.next.state)
            animator.animate()  # first frame
            self.assertEqual(an2, animator.current.state)
            animator.animate()  # second frame
            animator.animate()  # third frame
            animator.animate()  # first frame again

            # ================ Back to  First Animation ============== #
            animator.set(person=1)

    def test_animator_play_switching_anim_on_condition(self):
        an1 = Animation(
            self.e,
            [
                Frame(name="Fredkiss", duration=.3),
            ]
        )

        an2 = Animation(
            self.e,
            [
                Frame(name="Kitty", duration=.3),
            ]
        )

        animator = self.anim_c(an1, an2, )
        animator['person'] = 1

        # Setup Transitions
        animator.add_transition(an1, an2, C(person=2), C(person=1))

        switch_an2 = (lambda dt: animator.set(person=2), 1)
        assetTwo = (lambda dt: self.assertEqual("Kitty", self.e.name), 1.5)

        switch_an1 = (lambda dt: animator.set(person=1), 2)
        assertOne = (lambda dt: self.assertEqual("Fredkiss", self.e.name), 2.5)

        self.run_anim(animator, switch_an1, assertOne, assetTwo, switch_an2, end=5)
        self.assertEqual("Fredkiss", self.e.name)

    def test_animator_play_switching_anim_on_condition_for_not_looping_anim(self):
        an1 = Animation(
            self.e,
            [
                Frame(name="Fredkiss", duration=.3),
            ],
            loop=False
        )

        an2 = Animation(
            self.e,
            [
                Frame(name="Kitty", duration=.3),
            ],
            loop=False
        )

        animator = self.anim_c(an1, an2, )
        animator['person'] = 1

        # Setup Transitions
        animator.add_transition(an1, an2, C(person=2), C(person=1))


        check_an1 = (lambda dt: self.assertEqual("Fredkiss", self.e.name), 0.5)

        switch_an2 = (lambda dt: animator.set(person=2), 1)
        assetTwo = (lambda dt: self.assertEqual("Kitty", self.e.name), 1.5)

        switch_an1 = (lambda dt: animator.set(person=1), 2)
        assertOne = (lambda dt: self.assertEqual("Fredkiss", self.e.name), 2.5)

        self.run_anim(animator,
                      check_an1,
                      switch_an1,
                      assertOne,
                      assetTwo,
                      switch_an2,
                      end=5)
        self.assertEqual("Fredkiss", self.e.name)

    def test_animator_frame_by_frame_switching_anim_on_any_condition(self):
        an1 = Animation(
            self.e,
            [
                Frame(name="Fred", duration=.3),
                Frame(name="Kiss 3", duration=.3),
                Frame(name="The Boss", duration=.3),
            ]
        )

        an2 = Animation(
            self.e,
            [
                Frame(name="Hello", duration=.3),
                Frame(name="Kitty", duration=.3),
            ]
        )

        an3 = Animation(
            self.e,
            [
                Frame(name="Hello", duration=.3),
                Frame(name="Unknown", duration=.3),
            ]
        )

        animator = self.anim_c(an1, an2, an3)
        animator['person'] = 1

        # Setup Transitions
        # animator.add_transition(an1, an2, C(person=2), C(person=1))
        animator.add_transition(ANY, an3, C(person=3))
        animator.add_transition(ANY, an1, C(person=1))
        animator.add_transition(ANY, an2, C(person=2))

        for i in range(3):
            # ================= First Animation ===================== #
            animator.animate()  # first frame
            animator.animate()  # second frame
            animator.animate()  # third frame
            animator.animate()  # first again
            self.assertEqual(an1, animator.current.state)

            # ================ Third Animation ============== #
            animator.set(person=3)
            self.assertEqual(an3, animator.next.state)
            animator.animate()  # first frame
            self.assertEqual(an3, animator.current.state)
            animator.animate()  # second frame
            animator.animate()  # third frame
            animator.animate()  # first frame again

            # ================ Second Animation ===================== #
            animator.set(person=2)
            self.assertEqual(an2, animator.next.state)
            animator.animate()  # first frame
            self.assertEqual(an2, animator.current.state)
            animator.animate()  # second frame
            animator.animate()  # third frame
            animator.animate()  # first frame again

            # Back to first animation
            animator.set(person=1)


if __name__ == '__main__':
    unittest.main()
