from genetic import FitnessFunc, mutation, population_fitness, run_evolution
from client import *
# from random import choices, randint, randrange, random
import random
import numpy as np
import json
import os
# API_ENDPOINT = 'http://10.4.21.156'
# MAX_DEG = 11
# SECRET_KEY='jg3q0CzLVQl9Jsf4PmLIUjuxMK4yU7Vh4b6FzthUbocuLqpvGG'

POPULATION_SIZE = 10
MATING_POOL_SIZE = 6
GENE_LENGTH = 11
MUTATION_PROB = 0.4
TRAIN_WT = 1
NO_CHLD_SELECTED = 3
NO_INIT_SELECTED = 2

population = []
child_population = []
mating_pool = []
# [(genome, [fitness, error1, error2])]

ch11 = []
ch22 = []
child_cnt = 0


def generate_genome():
    return [0.0 for _ in range(GENE_LENGTH)]


def find_fitness(genome):
    error = get_errors(SECRET_KEY, list(genome))
    fitness = abs(error[0] * TRAIN_WT + error[1])

    return [fitness, error[0], error[1]]


def generate_population():

    global population
    population = []
    tmp = [generate_genome() for _ in range(POPULATION_SIZE)]
    for i in range(0, len(tmp)):
        tmp[i] = mutation(tmp[i])
        population.append((tmp[i], find_fitness(tmp[i])))


def compare(xx):
    return xx[1][0]


def generate_mating_pool():
    global population
    global mating_pool
    # population = sorted(population, key=compare)
    random.shuffle(population)
    mating_pool = population[:MATING_POOL_SIZE]
    np.random.shuffle(mating_pool)


def single_point_crossover(parent1, parent2):
    global ch11
    global ch22
    split_point = random.randint(1, GENE_LENGTH - 1)
    # return parent1[0:split_point] + parent2[split_point:], parent2[0:split_point] + parent1[split_point:]
    ch11 = parent1[0:split_point] + parent2[split_point:]
    ch22 = parent2[0:split_point] + parent1[split_point:]


def cross_over(parent1, parent2):
    global ch11
    global ch22
    alpha = 0.5
    ch11 = []
    ch22 = []
    for i in range(GENE_LENGTH):
        gamma = (1. + 2. * alpha) * random.random() - alpha
        ch11.append((1. - gamma) * parent1[i] + gamma * parent2[i])
        ch22.append(gamma * parent1[i] + (1. - gamma) * parent2[i])


def reproduce():
    global ch11
    global ch22
    global mating_pool
    global child_cnt
    p1 = random.randint(0, MATING_POOL_SIZE-1)
    p2 = random.randint(0, MATING_POOL_SIZE-1)

    print("REPRODUCTION")
    print("Parent 1")
    print(mating_pool[p1])
    print("Parent 2")
    print(mating_pool[p2])

    # single_point_crossover(mating_pool[p1][0], mating_pool[p2][0])
    cross_over(mating_pool[p1][0], mating_pool[p2][0])
    ch1 = ch11
    ch2 = ch22

    print("CHILD: " + str(child_cnt))
    print(ch1)
    ch1 = mutation(ch1)
    fitness_ch1 = find_fitness(ch1)
    print("MUTATED CHILD: " + str(child_cnt))
    print((ch1, fitness_ch1))
    child_cnt = child_cnt + 1

    print("CHILD: " + str(child_cnt))
    print(ch2)
    ch2 = mutation(ch2)
    fitness_ch2 = find_fitness(ch2)
    print("MUTATED CHILD: " + str(child_cnt))
    print((ch2, fitness_ch2))
    child_cnt = child_cnt + 1

    # save children
    # print(type(ch1))
    # print(ch1)
    # ch1 = mutation(ch1)
    # ch2 = mutation(ch2)

    # save mutated children

    child_population.append((ch1, fitness_ch1))
    child_population.append((ch2, fitness_ch2))


def get_mutated_value(genome, index):
    return vector_rank_12[index] * random.uniform(0.85, 1.15)


def mutation(genome):
    for _ in range(GENE_LENGTH):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random(
        ) > MUTATION_PROB else get_mutated_value(genome, index)
    return genome


def write_json(data, filename="best_vector_15.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def eliminate(GEN):
    global population
    global child_population
    # new_generation = np.concatenate((population, child_population))
    # new_generation = sorted(new_generation, key=compare)
    # new_generation = new_generation[:POPULATION_SIZE]
    # population = new_generation

    child_population = sorted(child_population, key=compare)
    population = sorted(population, key=compare)

    new_generation = []
    rest_generation = []
    for i in range(NO_CHLD_SELECTED):
        new_generation.append(child_population[i])
    for i in range(NO_CHLD_SELECTED, len(child_population)):
        rest_generation.append(child_population[i])

    for i in range(NO_INIT_SELECTED):
        new_generation.append(population[i])
    for i in range(NO_INIT_SELECTED, len(population)):
        rest_generation.append(population[i])

    rest_generation = sorted(rest_generation, key=compare)
    for i in range(POPULATION_SIZE - NO_CHLD_SELECTED - NO_INIT_SELECTED):
        new_generation.append(rest_generation[i])

    population = new_generation
    population = sorted(population, key=compare)
    new_generation = sorted(new_generation, key=compare)
    print("BEST VECTOR###@" + str(GEN))
    print(new_generation[0])
    # print(type(new_generation[0]))
    with open("best_vector_15.json") as json_file:
        data = json.load(json_file)
        # print(data)
        temp = data["best_vector"]
        rowDict = {
            "Generation": str(GEN),
            "Best Vector": new_generation[0],
            "Population": population
        }
        temp.append(rowDict)
        write_json(data)


def recalculate_fitness():
    global population

    for i in range(POPULATION_SIZE):
        genome = population[i]
        population[i] = (genome[0], find_fitness(genome[0]))


def run_evolution(gen_from=1, gen_to=1):
    global population
    global child_population
    global mating_pool
    if gen_from > gen_to:
        return
    # population = [([0.0, -1.4663600112199388e-12, 1.224957154210799e-13, 5.02097205148173e-11, -9.461609430650801e-11, -1.3847045204051619e-15, -1.4903196047433395e-16, 0.0, -1.6773631386534151e-06, 0.0, 6.967572098353319e-10], [363990574917.4227, 42943532916.40675, 321047042001.016]), ([0.0, -1.7402279534278152e-12, 1.209168938419586e-13, 5.822013033020788e-11, -1.1699721110625948e-10, -1.2881705511995002e-15, -1.1938291178866723e-16, 0.0, -1.696969382477944e-06, 0.0, 7.002747093470096e-10], [383869267418.47406, 63371968647.97536, 320497298770.4987]), ([0.0, -1.7171792613145792e-12, 9.642288013629758e-14, 2.2985873468245828e-12, -1.1462470701517557e-10, -1.3451017403002982e-15, -1.2851974736751085e-16, 0.0, -1.7076692702479355e-06, 0.0, 7.066647362360672e-10], [387893324048.71936, 59390853150.02582, 328502470898.69354]), ([0.0, -1.6963358975443985e-12, 1.245022909703573e-13, 1.0153751711442106e-11, -1.1442465246022158e-10, -1.3369817425324545e-15, -1.1635685745949742e-16, 0.0, -1.7056012491675042e-06, 0.0, 7.063477515121736e-10], [388600047389.21497, 55343718183.62588, 333256329205.5891]), ([0.0, -1.450533587664946e-12, 1.2095400840948277e-13, 4.07376038106633e-11, -1.3220306309026808e-10, -1.3095326226182863e-15, -1.3643314055529076e-16, 0.0, -1.7049003860169664e-06, 0.0, 7.044279915135451e-10], [389355175069.9248, 62024627692.99754, 327330547376.92725]), ([0.0, -1.844807071307767e-12, 1.2472662496489638e-13, 7.251037263200312e-11, -1.1654467388538106e-10, -1.2814981821125478e-15, -1.1547340083785246e-16, 0.0, -1.70159564299606e-06, 0.0, 7.030441875587854e-10], [390695111768.5732, 59158612429.97298, 331536499338.6002]), ([0.0, -1.6532621385668748e-12, 1.2128700665167287e-13, 4.0261462450246494e-11, -9.347284553370553e-11, -1.3213668165859425e-15, -1.2375577204920675e-16, 0.0, -1.7061751448978648e-06, 0.0, 7.063237221175045e-10], [391442759332.72723, 55779895590.17, 335662863742.55725]), ([0.0, -1.6777316420358537e-12, 1.0776613895932618e-13, -4.252139348449834e-12, -1.1896844015385917e-10, -1.3808930881069457e-15, -1.1927921585548596e-16, 0.0, -1.7161391699520994e-06, 0.0, 7.101202223968817e-10], [391953659469.28357, 65370769433.841515, 326582890035.4421]), ([0.0, -1.5146558297645956e-12, 1.2322440981858159e-13, 3.585872300172009e-11, -8.31857476132741e-11, -1.2995061489157618e-15, -1.254390954966658e-16, 0.0, -1.7065276177760228e-06, 0.0, 7.046125899292029e-10], [392365870943.0286, 64505005682.684494, 327860865260.3441]), ([0.0, -1.5683731222137906e-12, 1.1945339911887209e-13, -8.80159819308938e-12, -1.011794890681875e-10, -1.3636174623219998e-15, -1.4087024804624921e-16, 0.0, -1.7108897652409873e-06, 0.0, 7.097070730357297e-10], [392870143003.098, 52537179681.78836, 340332963321.3097]), ([0.0, -1.6666354581435405e-12, 1.2289141157639148e-13, 3.6334864362136895e-11, -1.2191596516983667e-10, -1.2876719549481055e-15, -1.1952271113516571e-16, 0.0, -1.7052528588951242e-06, 0.0, 7.027168593252434e-10], [394372163814.6095, 72004423486.05301, 322367740328.55646]), ([0.0, -1.800817431543342e-12, 1.156102756306383e-13, 9.89822774145686e-12, -1.2700768237415341e-10, -1.3273088919439123e-15, -1.3883284655772163e-16, 0.0, -1.7118251680247673e-06, 0.0, 7.088355795259502e-10], [396462273063.08655, 56656982148.24387, 339805290914.84265]), ([0.0, -1.574612349987716e-12, 1.0887962733822848e-13, 8.452150120648262e-11, -1.443870739823696e-10, -8.657880602051297e-16, -1.4874958469541043e-16, 0.0, -1.6995942418144319e-06, 0.0, 6.866308156341845e-10], [516881279046.1665, 133699310493.924, 383181968552.2425]), ([0.0, -1.623131742804388e-12, 1.2450562082088643e-13, 5.537278223495229e-11, -9.36031182612248e-11, -1.3875747682718228e-15, -1.4156361694586001e-16, 0.0, -1.7091247203879317e-06, 0.0, 6.909705732176797e-10], [748085461281.4563, 295361772643.30743, 452723688638.1488]), ([0.0, -1.5547336066371432e-12, 1.1383479365331402e-13, 6.735578028973669e-11, -1.0394407660395607e-10, -8.152516218920854e-16, -1.5800697449620178e-16, 0.0, -1.7130840171581958e-06, 0.0, 6.731710746115417e-10], [1262763708339.0842, 461085129002.26984, 801678579336.8143]), ([0.0, -1.5149098808096362e-12, 1.2360513713553231e-13, 5.938834556629409e-11, -8.795822797865907e-11, -1.5939838916557776e-15, -1.279055277831783e-16, 0.0, -1.7055177037622358e-06, 0.0, 6.799937254228595e-10], [1581351315426.9673, 704117711003.8351, 877233604423.1321]), ([0.0, -1.4726747581884256e-12, 1.0744234000841048e-13, 5.926121421901729e-11, -1.1049482240023875e-10, -1.36315505209115e-15, -1.2778973338324866e-16, 0.0, -1.5947386821856843e-06, 0.0, 6.981888550116889e-10], [2400857837262.4126, 512689108706.21063, 1888168728556.202]), ([0.0, -1.310286944273762e-12, 1.2644759641859891e-13, 7.181274764791739e-11, -1.1395269903828704e-10, -1.1305553089474172e-15, -1.330642629852985e-16, 0.0, -1.7752007223967653e-06, 0.0, 6.920981256136962e-10], [2445433294738.2725, 958765108179.6926, 1486668186558.5796]), ([0.0, -1.555522758722787e-12, 9.797327950842389e-14, 7.091593611436566e-11, -1.0493651427978534e-10, -6.520072187582125e-16, -1.5136125425141516e-16, 0.0, -1.568504768920576e-06, 0.0, 7.072388176909653e-10], [7837535884627.424, 2378629920021.3794, 5458905964606.045]), ([0.0, -1.7161443116007394e-12, 1.0882496193257169e-13, 6.963595717738983e-11, -1.1201270527062959e-10, -8.44755249873155e-16, -1.393636006138937e-16, 0.0, -1.70024763911586e-06, 0.0, 7.79731631740191e-10], [10505117668093.95, 3198316069966.814, 7306801598127.136])]
    # population = [([0.0, -1.7130037106739733e-12, 1.0104573058247149e-13, 4.693144303891498e-12, -1.0999559711055395e-10, -1.359515653369574e-15, -1.2014209258856715e-16, 0.0, -1.7204475751031546e-06, 0.0, 7.093364927151334e-10], [407545931976.9197, 83384045994.61044, 324161885982.3092]), ([0.0, -1.7591248360362424e-12, 1.0062301183007159e-13, 5.7602745022738175e-11, -1.0204854535158758e-10, -1.2895883693319938e-15, -1.1908350883024413e-16, 0.0, -1.6925049038607525e-06, 0.0, 6.932212480908106e-10], [414663788762.3635, 106476408410.23032, 308187380352.1332]), ([0.0, -1.7433728318239732e-12, 1.0108948538328834e-13, 7.757877368539829e-11, -1.2396516681327553e-10, -1.2023349583934826e-15, -1.1677771885204874e-16, 0.0, -1.73290728070083e-06, 0.0, 7.143066147175321e-10], [438551636298.2059, 72425476212.05, 366126160086.1559]), ([0.0, -1.7088190729837152e-12, 1.0771904809723569e-13, 9.893895046931932e-11, -1.2653468234024733e-10, -1.16026436728606e-15, -1.2055868672411272e-16, 0.0, -1.6981846695486896e-06, 0.0, 6.927929713232897e-10], [442438120822.2238, 111899857386.25288, 330538263435.97095]), ([0.0, -5.100311464712097e-13, 4.2824731853653965e-14, 6.852532940504661e-11, -1.3072111557595458e-10, -1.278060652521475e-15, -1.1946818590591276e-16, 0.0, -1.711392872511518e-06, 0.0, 7.004765269010706e-10], [444953511118.6394, 116118122698.60149, 328835388420.0379]), ([0.0, -1.492822446042872e-12, 1.0730804500446653e-13, 5.954930918784064e-11, -9.49554516971678e-11, -1.1721420232124084e-15, -1.2426947156961078e-16, 0.0, -1.7343392648414791e-06, 0.0, 7.137773433131701e-10], [445948964738.1146, 77478396302.96976, 368470568435.1449]), ([0.0, -1.492822446042872e-12, 1.01773840478343e-13, 5.954930918784064e-11, -9.49554516971678e-11, -1.1721420232124084e-15, -1.2426947156961078e-16, 0.0, -1.7343392648414791e-06, 0.0, 7.137773433131701e-10], [445948964738.1146, 77478396302.96976, 368470568435.1449]), ([0.0, -1.492822446042872e-12, 1.01773840478343e-13, 5.954930918784064e-11, -9.495545169716778e-11, -1.1721420232124084e-15, -1.2426947156961078e-16, 0.0, -1.7343392648414791e-06, 0.0, 7.137773433131701e-10], [445948964738.1146, 77478396302.96976, 368470568435.1449]), ([0.0, -1.5262983985110621e-12, 1.017279681248121e-13, 6.31200890993871e-11, -1.2536098466804962e-10, -1.1238237841278266e-15, -1.3372012784174693e-16, 0.0, -1.7348527629053589e-06, 0.0, 7.136294062284552e-10], [456948902785.9906, 77734752139.9103, 379214150646.0803]), ([0.0, -1.609143607709381e-12, 6.256549767698966e-14, 7.22082625879486e-11, -1.2594208555531986e-10, -1.1092125883632545e-15, -1.1946369293426536e-16, 0.0, -1.7353485060723228e-06, 0.0, 7.136329276626258e-10], [460901004036.4242, 78548803579.43044, 382352200456.9938]), ([0.0, -1.4725145650102455e-12, 1.068096940852135e-13, 5.883391099753524e-11, -1.0024697724051403e-10, -1.0561916538730471e-15, -1.3079956103482698e-16, 0.0, -1.7161243566879587e-06, 0.0, 7.001909778893567e-10], [462689818022.6636, 103272534788.15544, 359417283234.5081]), ([0.0, -1.5519376938694992e-12, 1.1456932526945984e-13, 1.0540447575946401e-10, -1.4314345751643474e-10, -9.05481470844897e-16, -1.227640490141382e-16, 0.0, -1.6999831636814552e-06, 0.0, 6.947402492073049e-10], [464047229587.00916, 84576190934.60397, 379471038652.40515]), ([0.0, -1.4658491219765397e-12, 2.7159725640970867e-14, 5.822736476408099e-11, -1.1669283670810007e-10, -9.220213328131102e-16, -1.2493889258873006e-16, 0.0, -1.7031940651525945e-06, 0.0, 6.970289658065876e-10], [466396052679.47424, 82132555596.28442, 384263497083.1898]), ([0.0, -1.3963756214789178e-12, 1.7013645916237578e-13, 6.869698287244282e-11, -1.0128194435333353e-10, -1.0655360920465555e-15, -1.2239339777042283e-16, 0.0, -1.7325725222481624e-06, 0.0, 7.109573346162767e-10], [466510141633.7474, 84009709358.2855, 382500432275.46185]), ([0.0, -1.7012454347362236e-12, 1.1093212713839161e-13, 7.999459335214827e-11, -1.2438550007640808e-10, -1.1942261355133354e-15, -1.243748928473681e-16, 0.0, -1.7069980012051173e-06, 0.0, 6.95448969591725e-10], [476820154904.28467, 133254816639.84964, 343565338264.435]), ([0.0, -1.7860789781696622e-12, 1.1037106580542695e-13, 7.095323329600224e-11, -1.1675957734083866e-10, -9.128503978530904e-16, -1.323300478909504e-16, 0.0, -1.6868123218373977e-06, 0.0, 7.017036180616889e-10], [689067575626.14, 108372515021.43869, 580695060604.7013]), ([0.0, -1.6237613929291803e-12, 1.303793879254249e-13, 4.895808928679206e-11, -9.781372639616628e-11, -1.0665971681676178e-15, -1.3485008253556217e-16, 0.0, -1.6305483890981967e-06, 0.0, 7.106074750298646e-10], [2826923007108.948, 686861492623.3586, 2140061514485.5894]), ([0.0, -1.5092315475238097e-12, 1.1060891967413139e-13, 1.1203001614886005e-10, -1.503490469888716e-10, -9.830975296465453e-16, -1.1613760541993015e-16, 0.0, -1.7460781225448876e-06, 0.0, 7.749816534416127e-10], [5242528330179.428, 1457318020900.835, 3785210309278.5923]), ([0.0, -1.7280477407525818e-12, 1.0772909440472503e-13, 5.4182225559968684e-11, -1.0817349147345902e-10, -1.0787891711353583e-15, -1.1421137258766275e-16, 0.0, -1.9279326157857815e-06, 0.0, 7.202725668032615e-10], [8082281265097.171, 3016435202732.4785, 5065846062364.692]), ([0.0, -1.8399838344334854e-12, 1.0530474972352232e-13, 7.286845950350436e-11, -1.0535898302015542e-10, -1.0618381566123953e-15, -1.2386686197209557e-16, 0.0, -1.9340967686020905e-06, 0.0, 7.066372005011508e-10], [11550663399803.04, 4276974339452.439, 7273689060350.6])]
    # recalculate_fitness()
    generate_population()
    # population = []

    for i in range(gen_from, gen_to+1):
        child_cnt = 1
        print("GENERATION #" + str(i))
        print("INITAL POPULATION")
        print(population)
        # save_pop
        child_population = []
        generate_mating_pool()
        # save_pool
        print("MATING POOL")
        print(mating_pool)
        for j in range(int(MATING_POOL_SIZE/2)):
            reproduce()

        eliminate(i)
        # save_final_pop
        print("FINAL POPULATION")
        print(population)
        print("END OF GENERATION #" + str(i))
        print("###")
        print("###")
        print("###")
        print("")


def try_best_vector():
    # GEN[30][0] Rank 37
    best_vect = [
                    0.0,
                    -1.7130037106739733e-12,
                    1.0104573058247149e-13,
                    4.693144303891498e-12,
                    -1.0999559711055395e-10,
                    -1.359515653369574e-15,
                    -1.2014209258856715e-16,
                    0.0,
                    -1.7204475751031546e-06,
                    0.0,
                    7.093364927151334e-10
                ]
    # GEN[62][0] Rank 39
    best_vect = [
                    0.0,
                    -1.7533516552208447e-12,
                    8.970705276124391e-14,
                    4.569613708968034e-13,
                    -1.3311042453551332e-10,
                    -1.4508265112492427e-15,
                    -1.166855096925426e-16,
                    0.0,
                    -1.6903069735908941e-06,
                    0.0,
                    7.006041543310762e-10
                ]
    # GEN[68][0] Rank 40
    best_vect = [
                    0.0,
                    -1.435707752540825e-12,
                    1.1196864218717943e-13,
                    -2.098755492102859e-11,
                    -9.430790272771325e-11,
                    -1.3819111142498968e-15,
                    -1.4666518286312518e-16,
                    0.0,
                    -1.6788941962274544e-06,
                    0.0,
                    6.961498814516326e-10
                ]
    # GEN[69][0] Rank 39
    best_vect = [
                    0.0,
                    -1.6898409223825058e-12,
                    1.0274026266644598e-13,
                    3.502478784701034e-11,
                    -1.2122197137070304e-10,
                    -1.503832089075339e-15,
                    -1.2766982072891354e-16,
                    0.0,
                    -1.6862801212317265e-06,
                    0.0,
                    7.002213837520733e-10
                ]
    # GEN[72][0] Rank 40
    best_vect = [
                    0.0,
                    -1.276389820440355e-12,
                    1.054270907847897e-13,
                    2.011892315735388e-11,
                    -9.67434191120709e-11,
                    -1.515827174054531e-15,
                    -1.5945387114427634e-16,
                    0.0,
                    -1.6759498834986141e-06,
                    0.0,
                    6.937724302212283e-10
                ]
    # Rank 43
    best_vect = [
                        0.0,
                        -1.380035132538791e-12,
                        1.3360238892681605e-13,
                        2.263572805707767e-11,
                        -1.4540006734896595e-10,
                        -1.431597382463194e-15,
                        -1.3316288306060277e-16,
                        0.0,
                        -1.6766386868309246e-06,
                        0.0,
                        7.158143656437061e-10
                    ]
    # Rank 19
    best_vect = [
                        0.0,
                        -1.9354290562743804e-12,
                        1.3802479173712625e-13,
                        2.701499857434608e-11,
                        -1.2959324095911062e-10,
                        -1.4087958133960406e-15,
                        -1.1874282729943896e-16,
                        0.0,
                        -1.693084306983949e-06,
                        0.0,
                        6.693780439888291e-10
                    ]
    # Rank 27
    best_vect = [
                        0.0,
                        -4.835044567160189e-13,
                        8.304303268283333e-14,
                        -3.5741170813129387e-12,
                        -1.2779225975089882e-10,
                        -9.566678396295409e-16,
                        -1.1852808555831912e-16,
                        0.0,
                        -1.7968610679476228e-06,
                        0.0,
                        7.317114155246566e-10
                    ]
    # Rank 8 vector now gives rank 17

    # Rank 16 GEN[9][2]
    best_vect = [
                        0.0,
                        -1.4801693324028387e-12,
                        3.897001129923237e-14,
                        6.716562478000572e-11,
                        2.9213979579084905e-12,
                        -1.0270597048298093e-16,
                        -1.3427072993973024e-16,
                        0.0,
                        -1.7298915011318982e-06,
                        0.0,
                        6.872228993668033e-10
                    ]
    # Rank 12 GEN[9][3]
    best_vect = [
                        0.0,
                        -1.597105924245191e-12,
                        2.198934018367277e-14,
                        3.491044484088095e-11,
                        6.855029194610278e-13,
                        0.0,
                        -6.726699633209086e-17,
                        0.0,
                        -1.7670843276135381e-06,
                        0.0,
                        6.955956541923088e-10
                    ]
    
    print(submit(SECRET_KEY, vector_rank_8))
    quit()


if __name__ == "__main__":
    # try_best_vector()
    run_evolution(1, 78)