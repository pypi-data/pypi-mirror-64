def get_prime_number():
    prime_numbers = []
    candidate = 2
    while True:
        if candidate <= 3:
            prime_numbers.append(candidate)
            yield candidate

        is_prime = True
        for prime_num in prime_numbers:
            if candidate % prime_num == 0:
                is_prime = False
                break


        if is_prime:
            prime_numbers.append(candidate)
            yield candidate

        candidate += 1
