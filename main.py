class Prime:

    def __init__(self, maxi, sieve=True, prime_decomp=True):
        """
        :param maxi: the maximum of our exploration range
        :param sieve: perform the Sieve of Eratosthenes on load

        primes: dict, value = True iff key is prime
        prime_divisors: dict, list of prime divisors and their multiplicities for each number in the range
        """
        self.maxi = maxi

        self.my_range = range(2, self.maxi + 1)
        self.primes = dict(
            zip(
                self.my_range,
                [True] * self.maxi
            )
        )

        # For each number in our range, the list of prime divisors with their multiplicities
        self.prime_divisors = dict(
            zip(
                self.my_range,
                [Divisors(n) for n in self.my_range]
            )
        )

        # Yields true iff the sieve has been performed until maxi
        self.sieved = False

        if sieve:
            self.sieve()

        if self.sieved and prime_decomp:
            self.get_prime_decomposition()

    def sieve(self):
        """
        Compute the Sieve of Eratosthenes and record the numbers' divisors
        """
        if self.sieved:
            return False

        prime = 2
        while prime < self.maxi:
            for alpha in range(2, self.maxi / prime + 1):
                n = alpha * prime
                self.primes[n] = False
                self.prime_divisors[n].add_divisor(prime)
                self.prime_divisors[n].add_divisor(alpha)

            # Get the new prime number
            prime += 1
            while prime < self.maxi and not self.primes[prime]:
                prime += 1

        self.sieved = True

    def get_primes(self):
        """
        :return: an ascending list of all the prime numbers until self.maxi
        """
        assert self.sieved
        return sorted([k for k, b in self.primes.iteritems() if b])

    def get_prime_decomposition(self):
        assert self.sieved
        for n in self.my_range:
            if not self.prime_divisors[n].is_complete(self.primes):
                for divisor, multiplicity in self.prime_divisors[n].iteritems():
                    if not self.primes[divisor]:
                        self.prime_divisors[n].add_divisors_of(
                            q=self.prime_divisors[divisor],
                            m=multiplicity
                        )
                self.prime_divisors[n].is_complete = True


class Divisors:

    def __init__(self, n):
        """
        :type n: int
        """
        self.n = n
        self.divisors = dict()
        self.is_complete = False

    def add_divisor(self, d, m=1):
        """
        :param d: divisor of self.n
        :type d: int
        :param m: multiplicity m
        :type m: int
        """
        self.divisors[d] = self.divisors[d] + m if d in self.divisors else m

    def remove_divisor(self, d, m=0):
        """
        :param d: divisor of self.n
        :type d: int
        :param m: multiplicity m
        :type m: int

        Removes the divisor d from the list, or decreases its multiplicity
        """
        assert d in self.divisors
        if m == 0 or m == self.divisors:
            del self.divisors[d]
        else:
            self.divisors[d] -= m

    def add_divisors_of(self, q, m=1):
        """
        :type q: Divisors
        """
        assert q.is_complete
        for prime_divisor, multiplicity in q.divisors.iteritems():
            self.add_divisor(
                d=prime_divisor,
                m=multiplicity * m
            )

    def is_complete(self, primes):
        """
        :type primes: dict
        :return:
        """
        if not self.is_complete:
            for divisor in self.divisors:
                if not primes[divisor]:
                    self.is_complete = False
                    return False
            self.is_complete = True
        return self.is_complete
