[![Open in MATLAB Online](https://www.mathworks.com/images/responsive/global/open-in-matlab-online.svg)](https://matlab.mathworks.com/open/github/v1?repo=FernandaAntunez/Practica2GD&project=https://github.com/FernandaAntunez/ProyectoFinal-Dinamica_del_VIH)

# Proyecto Final: Dinámica del VIH

## Información de los estudiantes
Fernanda Antúnez \[22211745]; 22211745@tectijuana.edu.mx, Carlos Ramirez \[22212267]; 22212267@tectijuana.edu.mz

Gemelos Digitales

Ingeniería Biomédica

## Docente
Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

Departamento de Ingeniería Eléctrica y Electrónica, Tecnológico Nacional de México/IT Tijuana, Blvd. Alberto Limón Padilla s/n, Tijuana, C.P. 22454, B.C., México.

## Descripción de la asignatura
La asignatura de Gemelos Digitales forma parte del plan de estudios de la carrera en Ingeniería Biomédica con la siguiente competencia general del curso: Formula el gemelo digital a través de datos experimentales para el desarrollo estrategias de control mediante teorías de sistemas dinámicos no lineales y la experimentación in silico. Esta asignatura pretende aportar al perfil del Ingeniero Biomédico la capacidad de realizar investigación científica en el área de Biología de Sistemas con la finalidad de dirigir y participar en equipos de trabajo interdisciplinarios en contextos nacionales e internacionales, así como de proporcionar soluciones informáticas para resolver problemas en el campo de la Ingeniería Biomédica con ética profesional.

En el contexto de sistemas dinámicos que describen sistemas biológicos o fisiológicos, el modelizado in silico es una extensión lógica de la experimentación in vitro controlada, es el resultado natural del gran aumento de la potencia computacional disponible a un costo que disminuye continuamente, combinando las ventajas de la experimentación in vivo e in vitro, sin someterse a las consideraciones éticas y la falta de control asociadas con los experimentos in vivo. A diferencia de los experimentos in vitro, que existen de forma aislada, los modelos in silico permiten incluir un conjunto prácticamente ilimitado de variables y parámetros, lo que hace que los resultados sean más aplicables en problemas del mundo real. La experimentación in silico ha dado lugar al paradigma denominado como "gemelos digitales" (en inglés digital twins); en esencia, los gemelos digitales son una réplica o representación digital de un proceso o sistema del mundo real, donde por replica se refiere a un modelo computacional desarrollado con base en datos experimentales y características especiales que le permiten conectar lo físico con lo virtual con el propósito de mejorar el rendimiento de un sistema, detectar y prevenir fallas, y realizar predicciones sobre su respuesta ante diferentes estímulos o escenarios de operación; una definición más formal establece que: un gemelo digital es un conjunto de modelos adaptativos que emulan el comportamiento de un sistema físico en un sistema virtual obteniendo datos en tiempo real para actualizarse a lo largo de su ciclo de vida; replica al sistema físico para predecir fallas y oportunidades de cambio, prescribir acciones en tiempo real para optimizar y/o mitigar eventos inesperados observando y evaluando el perfil operativo del sistema. En el campo particular de la Biología de Sistemas, un gemelo digital se presenta como un algoritmo o conjunto de algoritmos computacionales desarrollados con base en modelos mecanicistas de un organismo vivo, esto con el objetivo de emular su fisiología para ilustrar su dinámica en el corto y en el largo plazo, así como predecir su respuesta a diferentes estímulos endógenos y exógenos.

## Objetivo y descripción del sistema
   La infección por VIH es un trastorno inmunológico caracterizado por la invasión, replicación y destrucción progresiva de los linfocitos T CD4+ en el sistema inmunitario. Con el fin de caracterizar este fenómeno, el siguiente modelo matemático describe la interacción y evolución temporal de tres poblaciones celulares clave a lo largo de 70 días:  
- Células sanas y(t): Representan la población blanco primordial del virus (principalmente linfocitos T CD4+). Estas células cuentan con una capacidad intrínseca de renovación o crecimiento natural regulada por el parámetro r₃.  
 - Células afectadas x(t): Son aquellas células inmunitarias que ya han sido colonizadas por el virus y cuya maquinaria molecular ha sido secuestrada. Presentan una tasa de proliferación independiente denotada por r₁.  
 - Carga viral z(t): Representa los viriones libres en el torrente sanguíneo capaces de perpetuar el ciclo infeccioso , los cuales se replican o ingresan al sistema a una tasa r₅.  
    La dinámica de éstas tres poblaciones está descrita por las siguientes tres EDOs no lineales de primer orden:

	x = r₁x+r₂xyz,
	y = r₃y-r₄yz,
	z = r₅z-r₆xz,

    
Los parámetros biológicos que regulan las interacciones del sistema se definen a continuación:  
    r₁=Tasa de proliferación o crecimiento natural de las células infectadas (crecimiento exponencial independiente).  
    r₂=Tasa de amplificación por interacción (Representa cómo la presencia conjunta del virus y una alta densidad de células sanas acelera la regeneración de nuevas células infectadas).  
    r₃= Tasa de regeneración o crecimiento intrínseco de las células sanas.  
    r₄=Tasa de infección o mortalidad (Es la proporción de células sanas que son destruidas o transformadas al contacto con el virus).
    r₅=Tasa de replicación natural, liberación o ingreso del virus al sistema.  
    r₆=Tasa de aclaramiento o consumo viral. Representa la cantidad de virus libre que desaparece del medio al interactuar con las células ya infectadas (x), ya sea porque se agota al entrar a ellas o por algún mecanismo de competencia.   

Palabras clave: Carga Viral, Inestabilidad, Modelado matemático, Poblaciones Celulares, VIH.

## Actividades a realizar
1. Diseñar una gráfica de los 3 conjuntos de datos y selección	 	
2. Diseñar un diagrama biológico sobre la dinámica del sistema y la interacción entre sus variables con las figuras de https://bioart.niaid.nih.gov/ o https://www.biorender.com/.
3. Graficar el Modelo y predicción a 2t	  
4. Calcular equilibrios y estabilidad local
5. Descripcion del modelo

## Lista de archivos incluidos en el repositorio
1. Cuaderno computacional de MATLAB [.mlx].
2. Imágenes de las simulaciones [.pdf].
3. Análisis matemático [.pdf].
4. Diagrama biológico del sistema [.png].

## Referencias
\[1] P. A. Valle, Syllabus para Gemelos Digitales, Tecnológico Nacional de México / Instituto Tecnológico de Tijuana, Tijuana, B.C., México, 2025. Permalink: https://biomath.xyz/course/

\[2] Itik, M., & Banks, S. P. (2010). Chaos in a three-dimensional cancer model. international Journal of bifurcation and chaos, 20(01), 71-79. https://doi.org/10.1142/S0218127410025417

\[3] Bryan, Kurt. Differential equations: A toolbox for modeling the world. Simiode, 2022. Permalink: https://www.simiode.org/resources/8307 
