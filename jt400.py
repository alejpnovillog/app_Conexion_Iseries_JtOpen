try:
    import jpype
    import os
    from com_ibm_as400_accees.as400 import AS400
    from com_ibm_as400_accees.user import User
    from com_ibm_as400_accees.job import Job

except Exception as e:
    print(f'Falta algun modulo {e}')


class JT400(AS400, User, Job):

    """
    CALL  PGM(QCMD) para poder acceder sin restricciones de permisos
    """

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Constructor
    def __init__(self, server, username, pwd):

        """
        server    = Es la Ip del server
        username  = Es el usuario
        pwd       = Es la password  del usuario
        """

        # inicializamos la lista
        self.registros = list()

        # asignamos los parametros recibidos
        self.server, self.username, self.pwd = server, username, pwd

        # definimos el path la java virtual machine
        jvmpath = r'C:\Program Files\Java\jre1.8.0_331\bin\server\jvm.dll'

        # definimos el path del jt400
        jpype.addClassPath(r'C:\Users\anovillo\Desktop\Software\JtOpen\lib\*')
        #jarpath = r'C:\Users\anovillo\Desktop\Software\JtOpen\lib\jt400.jar'

        # asignamos el path de las clases java
        jarpath = jpype.getClassPath()

        # definimos donde se encuentra jt400
        jvmArg = f'-Djava.class.path={jarpath}'

        # arracamos la virtual machine
        jpype.startJVM(jvmpath, jvmArg)

        # asignamos el constructor del AS400 usuario y password
        AS400.__init__(self, self.server, self.username, self.pwd)

        # asigno el constructor de User
        User.__init__(self, self.system, self.username)

        # asigno el constructor de Job
        Job.__init__(self, self.system)

        # definimos el objeto CommandCall
        CommandCall = jpype.JClass('com.ibm.as400.access.CommandCall')

        # definimos una instancia de CommandCall
        cc = CommandCall(self.system)
