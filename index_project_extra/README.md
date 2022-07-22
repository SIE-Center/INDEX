# INDEX
Index:
Envió de Correos:
    Genera internamente un Excel con formato con todos los campos generados en la pestaña Reporte SMC IMMEX
    Adjunta el Excel en un correo que se enviara a:
    Todos los contactos configurados en la etapa
    Todos los correos de los forwarders , operadoras y agente aduanal del reporte (correo 1 si es tipo 24 correo2 si es tipo 36)
    Se eliminan correos duplicados
    El mensaje en el correo cambia según el tipo 24 o 36
    Se genera evidencia del correo enviado con todo y attachment en el historial
Pestaña Reporte SMC IMMEX
    Se agrega pestaña en Project tasks con un tree de datos que permite la importación en Excel
    Se agregan vista de busqueda que permita mostrar nombre y codigo d e los catálogos
    Se agregan campos relacionados a partners
    Se agregan algunas campos escondidos que se pueden mediante los 3 puntos
    Solo permite edicion en la primer etapa
    Solo permite agregar lineas que esten en el rango de 48 y 72 horas con respecto a la fecha ETA
    Solo muestra los agentes aduanales, forwarders y operadoras que tenga relacionados el cliente IMMex asociado a la tarea 
Configuración de Etapa en proyectos
    Se agrega el campo correos que permite seleccionar a que personas se le envía correo según la etapa
    Contactos
    Se agrega pestaña de proveedores para dar de alta proveedores tipo [('F', 'Forwarder'),('A', 'Agente Aduanal'),('T', 'Transportista'),('O', 'Operadora')]
    Se agrega un segundo correo
Pestaña de Validación:
Index
    Valida que el reporte tenga contenido
    Valida que el rango de horas este entre 48 y 72 horas
    Valida que el Correo haya sido enviado
    Si la tarea no esta en tiempo bloquea la tarea y manda mensaje al historico
    Anota usuario fecha y hora de la validación
    Agrega mensaje al histórico
    Cambia etapa a Forwarders

Forwarders
    Valida que el rango de horas este entre 48 y 72 horas
    Si la tarea no esta en tiempo bloquea la tarea y manda mensaje al historico
    Anota usuario fecha y hora de la validación
    Genera un listado de correo de los agentes aduanales en el reporte
    Encuentra el usuario asociado a esos agentes
    Les agrega una actividad ligada a la tarea
    Agrega mensaje al histórico
    Cambia etapa a Agente Aduanal
Agente Aduanal
    Valida que el rango de horas este entre 24y 38 horas
    Si la tarea no esta en tiempo bloquea la tarea y manda mensaje al historico
    Anota usuario fecha y hora de la validación
    Se agregan varios campos de validacion booleana (si o no) si no ha checado todos impide continuar
    Agrega mensaje al histórico
    Cambia etapa a Transportista
Transportistas
    Valida que el rango de horas este entre 24y 38 horas
    Si la tarea no esta en tiempo bloquea la tarea y manda mensaje al historico
    Anota usuario fecha y hora de la validación
    Se agregan campos para placa y nombre del conductor y se valida que estén llenos
    Agrega mensaje al histórico
Etapa Control de Flujo
	Baja:
    Agrega mensaje al histórico (baja de la tarea) 
	Marca la tarea como archivada
    Alta:
    Agrega mensaje al histórico (Alta de la tarea) 
	Marca la tarea como Activa
    Reinicio:
	Regresa la tarea a la primer etapa, borra la marca del envío del correo y elimina todas las evidencias de las etapas posteriores
Agrega mensaje al histórico (reinicio de la tarea) 
Seguridad
    Se agregan 4 permisos Especificos para usuarios ligados a los botones de validacion
        <!-- grupo para autorizar Index  -->
    <record id="group_index_auth" model="res.groups">
    <!-- grupo para autorizar Forwarder  -->
    <record id="group_Forwarder_auth" model="res.groups">
    <!-- grupo para autorizar Agente  -->
    <record id="group_agente_auth" model="res.groups">
    <!-- grupo para autorizar Transportista  -->
    <record id="group_trans_auth" model="res.groups">
