PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

  El script `wav2lp.sh` realiza la parametrización de una señal de voz usando coeficientes de predicción lineal. 

    - `sox`: "Sound eXchange" es una herramienta para realizar conversiones y manipulaciones de archivos de audio.
       Invocamos este comando con las siguientes opciones: `sox $inputfile -t raw -e signed -b 16 -`.

        - `-t raw`: Transformamos el fichero de entrada de tipo WAV a formato raw:
          
           ![image](https://github.com/juditsalavedra/P4/assets/125377500/dcf8337c-dfce-4cfe-8709-0be359ee03e9)


        - `-e signed`: Indicamos el tipo de codificación que queremos aplicar, en nuestro caso **signed integer**:
          
           ![image](https://github.com/juditsalavedra/P4/assets/125377500/d3438b1e-9a09-4c59-bd39-46c6e8554846)


        - `-b 16`: Establecemos el tamaño en bits de cada muestra de la codificación:
          
           ![image](https://github.com/juditsalavedra/P4/assets/125377500/1981bc86-885d-41ae-b100-784326dffdcd)


        - `-`: Envía el output a la salida estándar y para realiza una redirección al *pipeline*.
  

  En resumen, con esta instrucción estamos convirtiendo el fichero de audio WAVE a un formato raw de enteros de
  16 bits. Esta conversión es necesaria para emplear el programa x2x de SPKT.
    
   - `$X2X`: Este argumento contiene la invocación de x2x, el programa de SPTK que permite la conversión entre
      distintos formatos de  datos:
     
      ![image](https://github.com/juditsalavedra/P4/assets/125377500/c2f38d38-3760-480c-ac3b-c051ebcfd7db)


    En nuestro programa se introduce la salida de la instrucción anterior en la siguiente (`X2X +sf`) mediante un *pipeline*.
  
      - `+sf`: Con esta opción se indica que el tipo de entrada es short (2 bytes = 16 bits) y se establece la salida de tipo
        float (4 bytes = 32 bits).

    ![image](https://github.com/juditsalavedra/P4/assets/125377500/618678b8-5f07-48b9-bf71-f37f2d45dbea)


    - `$FRAME`: Este argumento contiene la llamada a la función *frame* de SPTK que divide el stream de entrada en tramas.
      
      ![image](https://github.com/juditsalavedra/P4/assets/125377500/e7ab94e4-0b4b-4449-ba2e-7338a3114b7d)


        - `-l`: Establece el número de muestras de cada trama.
        - `-p`: Indica el periodo de las tramas, es decir, cuántas muestras está desplazada la trama respecto de la anterior.

        Los valores utilizados en el script son los siguientes: `$FRAME -l 240 -p 80`

    - `$WINDOW`: Este argumento contiene la llamada a la función *window* de SPTK que aplica una ventana a cada trama.
    
    ![image](https://github.com/juditsalavedra/P4/assets/125377500/38ee5660-d8e4-4eeb-92e3-e906800370c1)


        Los valores utilizados en el script son los siguientes: `$WINDOW -l 240 -L 240`.
          - `-l`: Longitud de las tramas de entrada.
          - `-L`: Longitud de las tramas de salida.
     
    En nuestro caso, la longitud de las tramas de entrada y de salida es la misma (240 muestras). Como no aplicamos ninguna
    otra opción, la ventana por defecto es la Blackman.
  
    ![image](https://github.com/juditsalavedra/P4/assets/125377500/18ebb45e-4c95-4749-b7c6-16dd37fcc401)


    - `$LPC`: Este argumento contiene la llamada a la función *lpc* de SPTK que calcula los coeficientes de predicción lineal
       de las tramas  enventanadas de datos que se pasan como entrada a través del *pipeline*.

      ![image](https://github.com/juditsalavedra/P4/assets/125377500/e31f9235-c5ce-45c0-8654-f04029e95948)
      
        En el programa escribimos `$LPC -l 240 -m $lpc_order > $base.lp`
         - `-l`: Longitud de la trama. En nuestro caso 240 muestras.
         - `-m`: Orden de los coeficientes LPC.
         - Mediante `lpc_order > $base.lp` redirigimos la salida a un fichero con extensión *.lp*.



- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 51 del script `wav2lp.sh`).
  
  ![image](https://github.com/juditsalavedra/P4/assets/125377500/e9809c3d-832b-479b-bf15-dc13cd634e31)

  
  El procedimiento seguido en estas líneas de código es el siguiente:
    1. Obtener el número de columnas `ncol` mediante la suma del orden de los coeficientes más 1 de la ganancia.
       
    2. `$X2X +fa < $base.lp`: Los datos de `base.lp` se convierten mediante el programa x2x de float a texto (ASCII)
        y se redirige la salida mediante el *pipeline*.
       
    3. `wc -l`: Se cuentan las líneas de la información introducida con este comando de UNIX.
       
    4. `perl -ne 'print $_/'$ncol', "\n";'`: Utilizando un *pipeline* se introduce lo anterior en el comando perl, con
        el que se procesa la entrada y se realiza una operación aritmética. La opción `-ne` indica que se lee la entrada
        línea por línea. Luego, se imprime cada línea dividida por el valor de la variable $ncol y seguido de un salto de
        línea: `'print $_/'$ncol', "\n"`. Este resultado se le asigna a la variable `nrow`.
       
    5. Se construye la matriz *fmatrix* colocando el número de columnas y filas delante (la cabecera) y los datos después:
        - `echo $nrow $ncol`: Se imprimen los valores de las variables `$nrow` y `$ncol`. Estos valores se pasarán como
           entrada para el siguiente comando.
       
        - `$X2X +aI`:El comando $X2X con la opción `+aI`convierte la entrada de texto a números de tipo *unsigned int* (4 bytes).
          
        - `> $outputfile`: Utiliza el símbolo > para redirigir la salida del comando anterior y guardarla en el archivo
           especificado en la variable $outputfile.
       
        - `cat $base.lp >> $outputfile`: Utiliza el comando cat para concatenar el contenido del archivo `$base.lp` y agregarlo
           al final del `$outputfile` utilizando el operador de redirección >>. 

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |      |      |      |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
