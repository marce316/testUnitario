#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del proyecto
"""

import unittest
import sys
import os
from io import StringIO

def run_tests():
    """Ejecutar todos los tests unitarios"""
    # Configurar el path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Descubrir y ejecutar tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Ejecutar tests con reporte detallado
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        failfast=False
    )
    
    print("🧪 Ejecutando Tests Unitarios...")
    print("=" * 50)
    
    result = runner.run(suite)
    
    # Mostrar resultados
    output = stream.getvalue()
    print(output)
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE TESTS")
    print("=" * 50)
    print(f"✅ Tests ejecutados: {result.testsRun}")
    print(f"❌ Fallos: {len(result.failures)}")
    print(f"🚫 Errores: {len(result.errors)}")
    print(f"⏭️  Omitidos: {len(result.skipped)}")
    
    if result.failures:
        print("\n❌ FALLOS:")
        for test, traceback in result.failures:
            try:
                error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
                print(f"  - {test}: {error_msg}")
            except (IndexError, AttributeError):
                print(f"  - {test}: Error en el test")
    
    if result.errors:
        print("\n🚫 ERRORES:")
        for test, traceback in result.errors:
            try:
                error_lines = traceback.split('\n')
                error_msg = error_lines[-2] if len(error_lines) > 1 else "Error desconocido"
                print(f"  - {test}: {error_msg}")
            except (IndexError, AttributeError):
                print(f"  - {test}: Error en el test")
    
    # Calcular porcentaje de éxito
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 ¡Todos los tests pasaron!")
        elif success_rate >= 80:
            print("✨ ¡Buen trabajo! La mayoría de tests pasaron.")
        else:
            print("⚠️  Necesitas revisar algunos tests.")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)