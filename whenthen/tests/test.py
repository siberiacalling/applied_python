from unittest import TestCase

from whenthen import whenthen


class Test(TestCase):
    def test_base(self):
        @whenthen
        def test(number):
            return number

        @test.when
        def test(number):
            if number == 0:
                return True

        @test.then
        def test(number):
            return "Zero"

        self.assertEqual(12, test(12))
        self.assertEqual("Zero", test(0))

    def test_two_conditions(self):
        @whenthen
        def test(number):
            return number

        @test.when
        def test(number):
            if number == 0:
                return True

        @test.then
        def test(number):
            return "Zero"

        @test.when
        def test(number):
            if number < 0:
                return True

        @test.then
        def test(number):
            return "Negative"

        self.assertEqual(12, test(12))
        self.assertEqual("Zero", test(0))
        self.assertEqual("Negative", test(-1))

    def test_only_then(self):
        @whenthen
        def test(number):
            return number

        with self.assertRaises(ValueError):
            @test.then
            def test(number):
                return "Negative"

    def test_two_when(self):
        @whenthen
        def test(number):
            return number

        @test.when
        def test(number):
            if number == 0:
                return True

        with self.assertRaises(ValueError):
            @test.when
            def test(number):
                if number < 0:
                    return True

    def test_wrong_order(self):
        @whenthen
        def test(number):
            return number

        @test.when
        def test(number):
            if number == 0:
                return True

        @test.then
        def test(number):
            return "Zero"

        with self.assertRaises(ValueError):
            @test.then
            def test(number):
                return "Negative"
