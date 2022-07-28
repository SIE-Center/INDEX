# INDEX
Index:
Envió de Correos:
    Genera internamente un Excel con formato con todos los campos generados en la pestaña Reporte SMC IMMEX
    Incluye la imagen configurada en la configuracion de la etapa inicial
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
    Se agrega Transportista
    Validaciones .....muchas validaciones
Configuración de Etapa en proyectos
    Se agrega el campo correos que permite seleccionar a que personas se le envía correo según la etapa
    Contactos
    Se agrega pestaña de proveedores para dar de alta proveedores tipo [('F', 'Forwarder'),('A', 'Agente Aduanal'),('T', 'Transportista'),('O', 'Operadora')]
    Se agrega un segundo correo
    Se agrega Imagen para Exceles (Logo)
Pestaña de Validación:
Index
    Valida que el reporte tenga contenido
    Valida que el rango de horas no sea menor a 48
    Valida que el Correo haya sido enviado
    Si la tarea no esta en tiempo bloquea la tarea y manda mensaje al historico
    Agrega mensaje al histórico
    Cambia etapa a Forwarders
    crea todo el ciclo de validaciones por linea
    envia un correo a todos los partners configurados en la etapa

Forwarders
        1.- Solo el usuario u_forwarder puede ver y autorizar group_Forwarder_auth
        2.-Valida que no hayan menos de 38 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Manda actividades al agente aduanal del la línea
        5.-Pasa de Estapa
        6.-Envía Mensaje al Histórico
Agente Aduanal
        1.- Solo el usuario u_aduanal puede ver y autorizar group_agente_auth
        2.-Valida que no hayan menos de 24 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Manda actividades al transportista del la línea
        5.-Pasa de Estapa
        6.-Envía Mensaje al Histórico
Transportistas
        1.- Solo el usuario u_transportista puede ver y autorizar group_trans_auth
        2.-Valida que no hayan menos de 16 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Pasa de Estapa
        5.-Envía Mensaje al Histórico
Maniobras
        1.- Solo el usuario u_transportista puede ver y autorizar
        2.-Valida que haya  validado sus campos
        3.-Pasa de Estapa
        4.-Envía Mensaje al Histórico        
Etapa Control de Flujo por Tarea
	Baja Total:
        Agrega mensaje al histórico (baja de la tarea) 
        Marca la tarea como archivada
    Alta:
        Agrega mensaje al histórico (Alta de la tarea) 
        Marca la tarea como Activa
    Reinicio:
	    Regresa la tarea a la primer etapa, borra la marca del envío del correo y elimina todas las evidencias de las etapas posteriores
        deja mensaje en el historial
    Fin:
        verifica que todas las linea de validación esten en etapa Finalizada o Baja
        manda la tarea al ultimo stage
        manda correo a todos los contactos dados de alta en la etapa finalizada
        manda historial
Etapa Control de Flujo por renglon de validacion
    Baja:
        Marca el renglon como baja
    Reinicio:
        regresa el renglon a la etapa forwarder y limpia todas las validaciones
    
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
    <!-- grupo para MAESTRO  -->
    group_master_auth
