import 'package:flutter/material.dart';

/// Botón de retroceso personalizado con estilo consistente.
/// 
/// Uso:
/// ```dart
/// AppBar(
///   leading: CustomIconBack(),
///   title: Text('Detalle'),
/// )
/// ```
class CustomIconBack extends StatelessWidget {
  final Color color;
  final VoidCallback? onPressed;

  const CustomIconBack({
    Key? key,
    this.color = Colors.white,
    this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return IconButton(
      onPressed: onPressed ?? () => Navigator.pop(context),
      icon: Icon(
        Icons.arrow_back_ios,
        color: color,
        size: 22,
      ),
    );
  }
}
