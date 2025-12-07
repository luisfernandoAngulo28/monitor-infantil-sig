import 'package:flutter/material.dart';

/// Campo de texto personalizado con estilo consistente.
/// 
/// Uso:
/// ```dart
/// CustomTextField(
///   label: 'Email',
///   icon: Icons.email,
///   onChanged: (value) => setState(() => email = value),
/// )
/// ```
class CustomTextField extends StatelessWidget {
  final String label;
  final String? initialValue;
  final Function(String) onChanged;
  final IconData icon;
  final EdgeInsetsGeometry margin;
  final String? Function(String?)? validator;
  final Color backgroundColor;
  final TextInputType keyboardType;
  final bool obscureText;
  final TextEditingController? controller;
  final int maxLines;
  final String? hintText;

  const CustomTextField({
    Key? key,
    required this.label,
    required this.icon,
    required this.onChanged,
    this.margin = const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
    this.validator,
    this.backgroundColor = Colors.white,
    this.initialValue,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.controller,
    this.maxLines = 1,
    this.hintText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: margin,
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: TextFormField(
        controller: controller,
        initialValue: controller == null ? initialValue : null,
        onChanged: onChanged,
        obscureText: obscureText,
        validator: validator,
        keyboardType: keyboardType,
        maxLines: maxLines,
        style: const TextStyle(fontSize: 15),
        decoration: InputDecoration(
          labelText: label,
          hintText: hintText,
          labelStyle: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 14,
          ),
          prefixIcon: Icon(
            icon,
            color: const Color(0xFF2196F3),
            size: 22,
          ),
        ),
      ),
    );
  }
}
