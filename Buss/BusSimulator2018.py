import random
import contextlib
import copy
with contextlib.redirect_stdout(None):
    import pygame

BUS_MAX_SPEED = 15
BUS_ACC = 2
Simulation_Length = 1   # Measured in days
BUS_CAPACITY = 20


class BusStop:
    def __init__(self, position):
        self.waiting_people = []
        self.position = position
        self.popularity = random.randint(4*60, 10*60)

    def create_new_person(self, destination):
        self.waiting_people.append(Person(destination))


class Person:
    def __init__(self, destination):
        self.seconds_waited = 0
        self.transaction_time = random.randint(2, 30)
        self.destination = destination

    def tick(self):
        self.seconds_waited += 1


class Bus:
    def __init__(self, position):
        self.position = position
        self.velocity = BUS_MAX_SPEED
        self.passengers = []
        self.time_spent_on_passenger = 0
        self.capacity = BUS_CAPACITY
        self.current_bus_stop = None

    def drive(self, max_distance, throttle):
        self.position += self.velocity
        self.position %= max_distance

    def spend_time_on_consumer(self):
        self.time_spent_on_passenger += 1

    def distance_to_bus(self,bus, max_distance):
        if bus.position >= self.position:
            return bus.position - self.position
        else:
            return bus.position + max_distance - self.position


    def dump_passengers(self):
        arrived_passengers = []
        t = 0
        for pas in self.passengers:
            if pas.destination == self.current_bus_stop:
                arrived_passengers.append(pas)
        for p in arrived_passengers:
            t += p.seconds_waited
            self.passengers.remove(p)
        return t

    def arrive(self, bus_stop):
        self.current_bus_stop = bus_stop
        self.position = bus_stop.position


class World:
    def __init__(self, params):
        self.coord = 0      # How far down on the screen the world should be drawn
        self.strategy = 1
        self.params = params

        self.waited_time = 0
        number_of_bus_stops = random.randint(4, 10)
        self.bus_stops = []
        position = 0
        for bs in range(number_of_bus_stops):
            self.bus_stops.append(BusStop(position))
            position += random.randint(800, 10000)
        self.bus_stops[0].position = position

        number_of_buses = random.randint(4, 10)
        self.buses = []
        for a in range(number_of_buses):
            self.buses.append(Bus(self.bus_stops[0].position // number_of_buses * a))
            # Distributes buses equally throughout the circle.

    def create_passengers(self, seed):
        random.seed(seed)
        for st in range(len(self.bus_stops)):
            if random.randint(0, self.bus_stops[st].popularity) == 0:
                while True:
                    stop_number = random.randint(0, len(self.bus_stops) - 1)
                    if stop_number != st:
                        self.bus_stops[st].create_new_person(self.bus_stops[stop_number])
                        break

    def waited_time_of_existing_people(self):
        time = 0
        for bus in self.buses:
            for pas in bus.passengers:
                time += pas.seconds_waited
        for stop in self.bus_stops:
            for pas in stop.waiting_people:
                time += pas.seconds_waited
        return time

    def update_waiting_time(self):
        for bus in self.buses:
            for passenger in bus.passengers:
                passenger.tick()
        for stop in self.bus_stops:
            for passenger in stop.waiting_people:
                passenger.tick()

    def happen(self):
        for b in self.buses:
            if b.current_bus_stop is None:      # If the bus is not currently stopped at a bus stop
                if b.position < b.velocity:     # Check if the bus arrived to the first stop
                    b.arrive(self.bus_stops[0])
                    self.waited_time += b.dump_passengers()

                for s in self.bus_stops[1:]:             # Check if the bus arrived to any other bus stop
                    if b.position >= s.position > b.position - b.velocity:
                        b.arrive(s)
                        self.waited_time += b.dump_passengers()
                        break

            if b.current_bus_stop is not None:  # If the bus is at a stop and didn't just arrive
                if len(b.current_bus_stop.waiting_people) == 0 or len(b.passengers) >= b.capacity:
                    b.current_bus_stop = None

                else:
                    self.spend_time_general(b)

            if b.current_bus_stop is None:
                self.strat_general(b)
        self.update_waiting_time()

    def strat_lazy(self, bus):
        bus.drive(self.bus_stops[0].position, 1)

    def strat_general(self, bus):
        a = self.params[4] + self.params[5] * len(self.bus_stops) + self.params[6] * len(self.buses) + self.params[
            7] * len(bus.passengers)
        a /= 1 + len(self.bus_stops) + len(self.buses) + len(bus.passengers)
        for b in self.buses:
            if 0 < bus.distance_to_bus(b, self.bus_stops[0].position) < a * float(self.bus_stops[0].position) / len(self.buses):
                return
        bus.drive(self.bus_stops[0].position, 1)

    def spend_time_general(self, bus):
        a = self.params[0] + self.params[1] * len(self.bus_stops) + \
            self.params[2] * len(self.buses) + self.params[3] * len(bus.passengers)
        a /= 1 + len(self.bus_stops) + len(self.buses) + len(bus.passengers)
        for b in self.buses:
            if 0 > bus.distance_to_bus(b, self.bus_stops[0].position) > - a * self.bus_stops[0].position / len(self.buses):
                bus.drive(self.bus_stops[0].position, 1)
                return
        bus.spend_time_on_consumer()
        if bus.time_spent_on_passenger >= bus.current_bus_stop.waiting_people[0].transaction_time:
            bus.time_spent_on_passenger -= bus.current_bus_stop.waiting_people[0].transaction_time
            bus.passengers.append(bus.current_bus_stop.waiting_people.pop(0))


def draw(world, screen, images, fn):
    background = images[0]

    screen.blit(background, (0, world.coord))

    total_distance = world.bus_stops[0].position

    for stop in world.bus_stops:
        stop_position = int(stop.position / total_distance * 1400) + 4
        screen.blit(images[2], (stop_position, 210+world.coord))        # Draw bus stops
        for j in range(len(stop.waiting_people) // 5):
            screen.blit(images[4], (stop_position+2, 210 + 20*j + world.coord))       # Draw waiting people
        for j in range(len(stop.waiting_people) % 5):
            screen.blit(images[3], (stop_position + 2, 210 + 20 * j + 20 * (len(stop.waiting_people) // 5) + world.coord))
    for bus in world.buses:
        screen.blit(images[1], (int(bus.position / total_distance * 1400) + 4, 120 + world.coord))
        passenger_count = fn.render(str(len(bus.passengers)), True, (0, 0, 0))
        screen.blit(passenger_count, (int(bus.position / total_distance * 1400) + 4, 100 + world.coord))


def setup_graphics():
    # initialize the pygame module
    pygame.init()
    screen = pygame.display.set_mode((1400, 660))
    pygame.display.set_caption("Bus Simulator 2018")
    background = pygame.image.load("background.png").convert()

    red_bus_small = pygame.image.load("red_bus_small.png").convert()
    red_bus_small.set_colorkey((255, 255, 255))

    bus_stop = pygame.image.load("bus_stop.png").convert()
    bus_stop.set_colorkey((255, 255, 255))

    passenger = pygame.image.load("passenger.png").convert()
    passenger.set_colorkey((255, 255, 255))

    v_passenger = pygame.image.load("5_passengers.png").convert()
    v_passenger.set_colorkey((255, 255, 255))
    # pygame.display.set_icon(logo)
    images = [background, red_bus_small, bus_stop, passenger, v_passenger]

    font = pygame.font.SysFont("calibri", 14)

    return screen, images, font


def format_time(t):
    days = int(t / 86400)
    hours = int((t % 86400) / 3600)
    minutes = int((t % 3600) / 60)
    seconds = int(t % 60)
    return f"{days} dagar, {hours} timmar, {minutes} minutes, {seconds} sekunder"


def draw_time(t, screen, fn):
    time_text = fn.render(format_time(t), True, (0, 0, 0))
    screen.blit(time_text, (4, 4))


def run_test(strat_param1, strat_param2, graphics=False):
    if graphics:
        [screen, images, font] = setup_graphics()
    running = True
    world1 = World(strat_param1)
    world2 = copy.deepcopy(world1)
    world2.coord = 300
    worlds = [world1, world2]
    world1.strategy_param = strat_param1
    world2.strategy_param = strat_param2

    t = 0
    while running and t < Simulation_Length*86400:
        t += 1
        seed = random.random()
        for world in worlds:
            world.create_passengers(seed)
            world.happen()
        if graphics:
            for world in worlds:
                draw(world, screen, images, font)
            draw_time(t, screen, font)
            pygame.display.flip()
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print("Bussar och passagerare: ")
                    for b in world1.buses:
                        print(b.current_bus_stop)
                        for p in b.passengers:
                            print(p.destination.position)
    for world in worlds:
        world.waited_time += world.waited_time_of_existing_people()
        # print(f"{format_time(world.waited_time)}")
    if world1.waited_time < world2.waited_time:
        return 0
    else:
        return 1


def wannabe_ml(rounds):
    params = [random.uniform(0, 1), random.uniform(0, 1)]
    winners = []
    for e in range(1, rounds):
        wins = [0, 0]
        for f in range(1, 5):
            winner = run_test(1, params[0], 1, params[1])
            wins[winner] += 1
        if wins[0] >= wins[1]:
            params[1] = random.uniform(0, 1)
            winners.append(params[0])
            print(params[0])
        else:
            params[0] = random.uniform(0, 1)
            winners.append(params[1])
            print(str(params[1]) + ",")
    if wins[0] >= wins[1]:
        return params[0]
    else:
        return params[1]


if __name__ == '__main__':
    # print(wannabe_ml(25))
    run_test([0]*8, [0]*4 + [1]*3 + [0], True)
