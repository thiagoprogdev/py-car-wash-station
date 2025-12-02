from typing import List


class Car:
    def __init__(self, comfort_class: int, clean_mark: int, brand: str) -> None:
        """
        comfort_class: int 1..7
        clean_mark: int 1..10 (1 very dirty ... 10 perfectly clean)
        brand: car brand string
        """
        self.comfort_class = comfort_class
        self.clean_mark = clean_mark
        self.brand = brand

    def __repr__(self) -> str:
        return f"Car(comfort_class={self.comfort_class}, clean_mark={self.clean_mark}, brand={self.brand!r})"


class CarWashStation:
    def __init__(
        self,
        distance_from_city_center: float,
        clean_power: int,
        average_rating: float,
        count_of_ratings: int,
    ) -> None:
        """
        distance_from_city_center: float (1.0 .. 10.0)
        clean_power: int, the clean_mark level this station can achieve
        average_rating: float (1.0 .. 5.0), stored rounded to 1 decimal
        count_of_ratings: int
        """
        self.distance_from_city_center = float(distance_from_city_center)
        self.clean_power = int(clean_power)
        # store average rating rounded to 1 decimal as in examples
        self.average_rating = round(float(average_rating), 1)
        self.count_of_ratings = int(count_of_ratings)

    def calculate_washing_price(self, car: Car) -> float:
        """
        Calcula o custo de lavar um carro individualmente:
        comfort_class * (clean_power - car.clean_mark) * average_rating / distance_from_city_center
        Retorna o valor arredondado para 1 casa decimal.
        Se car.clean_mark >= clean_power, retorna 0.0 (não precisa lavar).
        NÃO modifica o carro.
        """
        diff = self.clean_power - car.clean_mark
        if diff <= 0:
            return 0.0
        if self.distance_from_city_center == 0:
            # evitar divisão por zero; interpretar como custo infinito não faz sentido aqui,
            # então retornamos 0.0 como fallback, mas idealmente distance nunca é 0.
            return 0.0
        price = (
            car.comfort_class * diff * self.average_rating / self.distance_from_city_center
        )
        return round(price, 1)

    def wash_single_car(self, car: Car) -> float:
        """
        Lava um único carro: se self.clean_power > car.clean_mark, atualiza
        car.clean_mark para self.clean_power e retorna o preço cobrado (arredondado).
        Caso contrário, não faz nada e retorna 0.0.
        """
        price = self.calculate_washing_price(car)
        if price > 0.0:
            # atualizar o carro depois de calcular o preço com o clean_mark original
            car.clean_mark = self.clean_power
        return price

    def serve_cars(self, cars: List[Car]) -> float:
        """
        Recebe uma lista de Car e lava apenas aqueles com car.clean_mark < self.clean_power.
        Retorna a receita total obtida, arredondada para 1 casa decimal.
        Modifica os carros lavados (seu clean_mark passa a ser self.clean_power).
        """
        total = 0.0
        for car in cars:
            if car.clean_mark < self.clean_power:
                total += self.wash_single_car(car)
        return round(total, 1)

    def rate_service(self, rating: float) -> None:
        """
        Adiciona uma nova avaliação única (rating) e atualiza average_rating e
        count_of_ratings. average_rating é armazenado arredondado para 1 casa decimal.
        """
        # novo average = (avg * count + rating) / (count + 1)
        new_total = self.average_rating * self.count_of_ratings + float(rating)
        self.count_of_ratings += 1
        self.average_rating = round(new_total / self.count_of_ratings, 1)


if __name__ == "__main__":
    # Exemplos do enunciado e checagens

    # Caso 1
    bmw = Car(comfort_class=3, clean_mark=3, brand="BMW")
    audi = Car(comfort_class=4, clean_mark=9, brand="Audi")

    wash_station = CarWashStation(
        distance_from_city_center=5,
        clean_power=6,
        average_rating=3.5,
        count_of_ratings=6,
    )

    income = wash_station.serve_cars([bmw, audi])
    assert income == 6.3, f"esperado 6.3, obteve {income}"
    assert bmw.clean_mark == 6
    assert audi.clean_mark == 9  # não foi lavado

    # Caso 2: ambos lavados
    bmw = Car(comfort_class=3, clean_mark=3, brand="BMW")
    audi = Car(comfort_class=4, clean_mark=2, brand="Audi")

    wash_station = CarWashStation(
        distance_from_city_center=5,
        clean_power=6,
        average_rating=3.5,
        count_of_ratings=6,
    )

    income = wash_station.serve_cars([bmw, audi])
    assert income == 17.5, f"esperado 17.5, obteve {income}"
    assert bmw.clean_mark == 6
    assert audi.clean_mark == 6

    # Exemplo maior
    bmw = Car(3, 3, "BMW")
    audi = Car(4, 9, "Audi")
    mercedes = Car(7, 1, "Mercedes")

    ws = CarWashStation(6, 8, 3.9, 11)
    income = ws.serve_cars([bmw, audi, mercedes])
    assert income == 41.7, f"esperado 41.7, obteve {income}"
    assert bmw.clean_mark == 8
    assert audi.clean_mark == 9  # não lavado
    assert mercedes.clean_mark == 8

    ford = Car(2, 1, "Ford")
    wash_cost = ws.calculate_washing_price(ford)
    assert wash_cost == 9.1, f"esperado 9.1, obteve {wash_cost}"
    assert ford.clean_mark == 1  # não modificado

    ws.rate_service(5)
    assert ws.count_of_ratings == 12
    assert ws.average_rating == 4.0

    print("All example assertions passed.")
