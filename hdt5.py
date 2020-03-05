#Oscar Paredez 19109

import random
import simpy
from statistics import stdev
from math import sqrt

env = simpy.Environment()
#Cambiar capacity a cpu para ir probando
cpu = simpy.Resource(env, capacity=1)
#cambiar init a ram para ir probando
ram = simpy.Container(env, capacity=100, init=100)
listaTiempo = []

def proceso(env, cpu, ram, num_inst, num_ram):
    #solicitar ram
    print ("# de instruccion: ",num_inst,"\n", "ram disponible: ",num_ram,"\n","nivel de la ram: ",ram.level,"\n")
    tiempo_inicial = env.now
    
    with ram.get(num_ram) as memoria:
        yield memoria

        while num_inst > 2:
            #solicitar al cpu
            with cpu.request() as turno:
                yield turno
                #esperar al turno respectivo
                
                yield env.timeout(1)
                
                #realizar simulacion
                num_inst-=3

            #retornar variable cpu
            r = random.randint(1,2)
            if r == 2:
                #simular procesos in/out
                yield env.timeout(1)
                
    ram.put(num_ram)
    tiempo_final = env.now - tiempo_inicial
    listaTiempo.append(tiempo_final)
    print("El tiempo final del proceso es: ",tiempo_final,"\n")
        
#retornar el total de ram al terminar el proceso

#Este intervalo es el que va cambiando
intervalo = 25
def process_generator(env, cpu, ram):
    
    for i in range(intervalo):
        env.process(proceso(env, cpu, ram, random.randint(1, 10), random.randint(1, 10)))
        yield env.timeout(random.expovariate(1/1))
        
env.process(process_generator(env, cpu, ram))
env.run()

tiempoPromedio = sum(listaTiempo)/intervalo
print("El promedio del tiempo es: ",tiempoPromedio)

desvEst = stdev(listaTiempo)
print ("La desviacion estandar de la muestra es ", desvEst)