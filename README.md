# State Safe Bank Integridad

Un módulo de Python que demuestra cómo utilizar criptografía (RSA + SHA-256) para garantizar la integridad y autenticidad de transacciones bancarias.

## 📋 Descripción

Este proyecto simula un sistema de protección de transacciones bancarias mediante:

- **Generación de claves RSA** (2048 bits) para cifrado asimétrico
- **Firmas digitales RSA-PSS** para autenticar transacciones
- **Hashing SHA-256** para detectar cualquier modificación
- **Detección de alteraciones** en datos financieros

## 🎯 Funcionamiento

El script realiza las siguientes operaciones:

1. Genera un par de claves RSA (privada/pública)
2. Crea una transacción bancaria de ejemplo
3. Calcula el hash SHA-256 de la transacción
4. Firma digitalmente la transacción con la clave privada
5. Verifica que la firma sea válida con la clave pública
6. Altera intencionalmente los datos de la transacción
7. Demuestra que la firma ahora no es válida (detecta la alteración)

## 📦 Requisitos

- Python 3.8+
- Librería `cryptography`

## 🚀 Instalación

```bash
pip install cryptography
```

## 🏃 Uso

Simplemente ejecuta el script:

```bash
python state_safe_bank_integridad.py
```

## 📂 Estructura de directorios generados

El script automáticamente crea:

```
state_safe_bank_integridad/
├── keys/
│   ├── private_key.pem      # Clave privada RSA (2048 bits)
│   └── public_key.pem       # Clave pública RSA
└── data/
    ├── transaccion_original.json      # Transacción sin modificar
    ├── transaccion_alterada.json      # Transacción modificada (demo)
    └── firma_transaccion.bin          # Firma digital de la transacción original
```

## 📊 Salida del script

El script mostrará:

- **Transacción Original**: Hash SHA-256 y validación de firma ✓
- **Transacción Alterada**: Hash diferente y firma inválida ✗
- **Comparación Final**: Evidencia de que cualquier cambio es detectado

## 🔐 Conceptos de Seguridad

- **Firma Digital (RSA)**: Garantiza autenticidad y no repudio
- **Hash SHA-256**: Detecta cualquier modificación en los datos
- **Criptografía Asimétrica**: Solo quien tiene la clave privada puede firmar
- **Integridad de Datos**: Cualquier alteración invalida la firma

## 💡 Caso de Uso

Este código es útil para:
- Proteger transacciones financieras
- Garantizar autenticidad de documentos
- Auditoría y cumplimiento normativo
- Educación en criptografía aplicada

## ⚙️ Funciones principales

- `generate_keys_if_missing()`: Genera claves RSA si no existen
- `sign_data()`: Firma datos con clave privada
- `verify_signature()`: Verifica firma con clave pública
- `calculate_sha256()`: Calcula hash de datos
- `canonical_json_bytes()`: Convierte JSON a representación canónica

## 📝 Ejemplo de salida

```
================================================================================

TRANSACCIÓN ORIGINAL

================================================================================
Archivo JSON:       data/transaccion_original.json
Hash SHA-256:       a1b2c3d4e5f6...
Archivo de firma:   data/firma_transaccion.bin
Firma válida:       SÍ

================================================================================

TRANSACCIÓN ALTERADA

================================================================================
Archivo JSON:       data/transaccion_alterada.json
Hash SHA-256:       x9y8z7w6v5u4...
Firma válida:       NO

================================================================================

COMPARACIÓN FINAL

================================================================================
¿El hash cambió?:   SÍ
¿Se detectó alteración?: SÍ, la verificación falló
```

## 🔒 Notas de Seguridad

- Las claves privadas se guardan sin encriptación (solo para demo)
- En producción, las claves deben estar protegidas
- Usa `encryption_algorithm` en lugar de `NoEncryption()` para produción
- Implementa contraseñas para las claves privadas

## 📄 Licencia

Este proyecto es de código abierto para propósitos educativos.

## 👤 Autor

Alen Armi

---

**¿Preguntas?** Consulta la documentación de [cryptography](https://cryptography.io/) para más detalles sobre RSA y firmas digitales.