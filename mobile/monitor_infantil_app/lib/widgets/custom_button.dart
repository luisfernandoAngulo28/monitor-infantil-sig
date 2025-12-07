import 'package:flutter/material.dart';

/// Botón personalizado reutilizable con estilo consistente.
/// 
/// Uso:
/// ```dart
/// CustomButton(
///   text: 'Iniciar Sesión',
///   onPressed: () => login(),
///   icon: Icons.login,
/// )
/// ```
class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Color color;
  final Color textColor;
  final EdgeInsetsGeometry margin;
  final double? width;
  final double height;
  final IconData? icon;
  final Color iconColor;
  final bool isLoading;

  const CustomButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.color = const Color(0xFF2196F3), // Azul Material
    this.textColor = Colors.white,
    this.margin = const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
    this.height = 50,
    this.width,
    this.icon,
    this.iconColor = Colors.white,
    this.isLoading = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      width: width ?? MediaQuery.of(context).size.width,
      margin: margin,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          disabledBackgroundColor: color.withOpacity(0.6),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          elevation: 3,
        ),
        child: isLoading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                ),
              )
            : Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (icon != null) ...[
                    Icon(icon, color: iconColor, size: 24),
                    const SizedBox(width: 8),
                  ],
                  Text(
                    text,
                    style: TextStyle(
                      color: textColor,
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}
