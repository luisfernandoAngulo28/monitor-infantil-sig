import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import '../models/nino.dart';

/// Pantalla para registrar un nuevo niño y vincular su dispositivo GPS.
/// 
/// Permite al tutor ingresar:
/// - Datos personales del niño (nombre, apellidos, fecha de nacimiento)
/// - ID del dispositivo GPS (IMEI) para tracking con Traccar
/// - Centro educativo al que asiste
class RegistroNinoScreen extends StatefulWidget {
  const RegistroNinoScreen({Key? key}) : super(key: key);

  @override
  State<RegistroNinoScreen> createState() => _RegistroNinoScreenState();
}

class _RegistroNinoScreenState extends State<RegistroNinoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _apiService = ApiService();
  
  // Controllers
  final _nombreController = TextEditingController();
  final _apellidoPaternoController = TextEditingController();
  final _apellidoMaternoController = TextEditingController();
  final _dispositivoIdController = TextEditingController();
  final _fechaNacimientoController = TextEditingController();
  
  // State
  DateTime? _fechaNacimiento;
  String _sexo = 'M';
  bool _trackingActivo = true;
  bool _isLoading = false;
  int? _centroEducativoId;
  List<CentroEducativo> _centrosEducativos = [];
  bool _loadingCentros = true;

  @override
  void initState() {
    super.initState();
    _cargarCentrosEducativos();
  }

  @override
  void dispose() {
    _nombreController.dispose();
    _apellidoPaternoController.dispose();
    _apellidoMaternoController.dispose();
    _dispositivoIdController.dispose();
    _fechaNacimientoController.dispose();
    super.dispose();
  }

  Future<void> _cargarCentrosEducativos() async {
    try {
      final centros = await _apiService.obtenerCentrosEducativos();
      setState(() {
        _centrosEducativos = centros;
        _loadingCentros = false;
        // Seleccionar el primer centro por defecto si hay alguno
        if (centros.isNotEmpty) {
          _centroEducativoId = centros.first.id;
        }
      });
    } catch (e) {
      setState(() {
        _loadingCentros = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error al cargar centros educativos: $e'),
            backgroundColor: Colors.orange,
          ),
        );
      }
    }
  }

  Future<void> _seleccionarFecha() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now().subtract(const Duration(days: 365 * 5)),
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
      locale: const Locale('es', 'ES'),
    );

    if (picked != null) {
      setState(() {
        _fechaNacimiento = picked;
        _fechaNacimientoController.text = DateFormat('dd/MM/yyyy').format(picked);
      });
    }
  }

  Future<void> _registrarNino() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    if (_fechaNacimiento == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Por favor selecciona la fecha de nacimiento'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final ninoData = <String, dynamic>{
        'nombre': _nombreController.text.trim(),
        'apellido_paterno': _apellidoPaternoController.text.trim(),
        'apellido_materno': _apellidoMaternoController.text.trim(),
        'fecha_nacimiento': DateFormat('yyyy-MM-dd').format(_fechaNacimiento!),
        'sexo': _sexo,
        'tracking_activo': _trackingActivo,
      };
      
      // Solo agregar centro_educativo si tiene valor
      if (_centroEducativoId != null) {
        ninoData['centro_educativo'] = _centroEducativoId;
      }
      
      // Solo agregar dispositivo_id si no está vacío
      if (_dispositivoIdController.text.trim().isNotEmpty) {
        ninoData['dispositivo_id'] = _dispositivoIdController.text.trim();
      }

      final nino = await _apiService.crearNino(ninoData);

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('✅ ${nino.nombreCompleto} registrado exitosamente'),
          backgroundColor: Colors.green,
        ),
      );

      // Volver a la pantalla anterior
      Navigator.pop(context, true);
    } catch (e) {
      if (!mounted) return;
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al registrar: ${e.toString()}'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Registrar Hijo/a'),
        backgroundColor: Colors.blue,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Información
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          children: [
                            Icon(
                              Icons.child_care,
                              size: 48,
                              color: Colors.blue,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Datos del Niño/a',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Ingresa la información de tu hijo/a',
                              style: Theme.of(context).textTheme.bodyMedium,
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Nombre
                    TextFormField(
                      controller: _nombreController,
                      decoration: const InputDecoration(
                        labelText: 'Nombre *',
                        hintText: 'Ej: Juan Carlos',
                        prefixIcon: Icon(Icons.person),
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'El nombre es obligatorio';
                        }
                        return null;
                      },
                      textCapitalization: TextCapitalization.words,
                    ),
                    const SizedBox(height: 16),

                    // Apellido Paterno
                    TextFormField(
                      controller: _apellidoPaternoController,
                      decoration: const InputDecoration(
                        labelText: 'Apellido Paterno *',
                        hintText: 'Ej: García',
                        prefixIcon: Icon(Icons.badge),
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'El apellido paterno es obligatorio';
                        }
                        return null;
                      },
                      textCapitalization: TextCapitalization.words,
                    ),
                    const SizedBox(height: 16),

                    // Apellido Materno
                    TextFormField(
                      controller: _apellidoMaternoController,
                      decoration: const InputDecoration(
                        labelText: 'Apellido Materno',
                        hintText: 'Ej: López (opcional)',
                        prefixIcon: Icon(Icons.badge_outlined),
                        border: OutlineInputBorder(),
                      ),
                      textCapitalization: TextCapitalization.words,
                    ),
                    const SizedBox(height: 16),

                    // Fecha de Nacimiento
                    TextFormField(
                      controller: _fechaNacimientoController,
                      decoration: const InputDecoration(
                        labelText: 'Fecha de Nacimiento *',
                        prefixIcon: Icon(Icons.calendar_today),
                        border: OutlineInputBorder(),
                        hintText: 'Toca para seleccionar',
                        suffixIcon: Icon(Icons.arrow_drop_down),
                      ),
                      readOnly: true,
                      onTap: _seleccionarFecha,
                      validator: (value) {
                        if (_fechaNacimiento == null) {
                          return 'La fecha de nacimiento es requerida';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    // Sexo
                    const Text(
                      'Sexo *',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: RadioListTile<String>(
                            title: const Text('Masculino'),
                            value: 'M',
                            groupValue: _sexo,
                            onChanged: (value) {
                              setState(() {
                                _sexo = value!;
                              });
                            },
                          ),
                        ),
                        Expanded(
                          child: RadioListTile<String>(
                            title: const Text('Femenino'),
                            value: 'F',
                            groupValue: _sexo,
                            onChanged: (value) {
                              setState(() {
                                _sexo = value!;
                              });
                            },
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),

                    // Centro Educativo
                    DropdownButtonFormField<int>(
                      value: _centroEducativoId,
                      decoration: const InputDecoration(
                        labelText: 'Kinder/Colegio (Opcional)',
                        prefixIcon: Icon(Icons.school),
                        border: OutlineInputBorder(),
                        helperText: 'Área segura para notificaciones',
                      ),
                      items: _loadingCentros
                          ? []
                          : [
                              const DropdownMenuItem<int>(
                                value: null,
                                child: Text('Sin asignar'),
                              ),
                              ..._centrosEducativos.map((centro) {
                                return DropdownMenuItem<int>(
                                  value: centro.id,
                                  child: Text(centro.nombre ?? 'Centro ${centro.id}'),
                                );
                              }),
                            ],
                      onChanged: (value) {
                        setState(() {
                          _centroEducativoId = value;
                        });
                      },
                    ),
                    const SizedBox(height: 24),

                    // Sección GPS
                    const Divider(),
                    const SizedBox(height: 16),
                    Text(
                      '📱 Dispositivo GPS (Opcional)',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Si tu hijo/a usa Traccar Client en su teléfono, ingresa el IMEI o ID del dispositivo.',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    const SizedBox(height: 16),

                    // Dispositivo ID (IMEI)
                    TextFormField(
                      controller: _dispositivoIdController,
                      decoration: const InputDecoration(
                        labelText: 'ID del Dispositivo (IMEI)',
                        hintText: 'Ej: 862104056214397',
                        prefixIcon: Icon(Icons.smartphone),
                        border: OutlineInputBorder(),
                        helperText: 'IMEI del teléfono con Traccar Client',
                      ),
                      keyboardType: TextInputType.number,
                    ),
                    const SizedBox(height: 16),

                    // Tracking Activo
                    SwitchListTile(
                      title: const Text('Activar Tracking GPS'),
                      subtitle: const Text(
                        'Permitir seguimiento en tiempo real',
                      ),
                      value: _trackingActivo,
                      onChanged: (value) {
                        setState(() {
                          _trackingActivo = value;
                        });
                      },
                      secondary: Icon(
                        _trackingActivo ? Icons.gps_fixed : Icons.gps_off,
                        color: _trackingActivo ? Colors.green : Colors.grey,
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Botón Registrar
                    ElevatedButton.icon(
                      onPressed: _registrarNino,
                      icon: const Icon(Icons.add_circle),
                      label: const Text('Registrar Hijo/a'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        textStyle: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
