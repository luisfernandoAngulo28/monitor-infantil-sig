import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/ninos_provider.dart';
import '../providers/auth_provider.dart';
import 'mapa_screen.dart';
import 'mapa_realtime_screen_example.dart';
import 'alertas_screen.dart';
import 'login_screen.dart';
import 'registro_nino_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    // Cargar datos al iniciar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<NinosProvider>(context, listen: false).cargarNinos();
    });
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      const MapaRealTimeScreen(), // Pantalla con WebSocket en tiempo real
      const AlertasScreen(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Monitor Infantil'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              Provider.of<NinosProvider>(context, listen: false).cargarNinos();
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              final confirm = await showDialog<bool>(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Cerrar Sesión'),
                  content: const Text('¿Está seguro que desea salir?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context, false),
                      child: const Text('CANCELAR'),
                    ),
                    TextButton(
                      onPressed: () => Navigator.pop(context, true),
                      child: const Text('SALIR'),
                    ),
                  ],
                ),
              );

              if (confirm == true && mounted) {
                await Provider.of<AuthProvider>(context, listen: false).logout();
                if (mounted) {
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(builder: (_) => const LoginScreen()),
                  );
                }
              }
            },
          ),
        ],
      ),
      body: screens[_currentIndex],
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const RegistroNinoScreen(),
            ),
          );
        },
        icon: const Icon(Icons.person_add),
        label: const Text('Registrar Niño'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.map),
            label: 'Mapa',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.notifications),
            label: 'Alertas',
          ),
        ],
      ),
    );
  }
}
