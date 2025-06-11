# KIBA

Este proyecto requiere la variable de entorno `SECRET_KEY` para firmar los tokens JWT.

## Desarrollo

Puedes definirla temporalmente en tu terminal antes de ejecutar la aplicación:

```bash
export SECRET_KEY="tu_clave_de_desarrollo"
```

## Producción

En producción se recomienda establecer `SECRET_KEY` como una variable de entorno del sistema o utilizar herramientas de gestión de secretos para asignar un valor seguro.

