import 'package:flutter/material.dart';
import 'package:youme_app/models/usage_history.dart';

class UsageList extends StatelessWidget {
  final List<UsageHistory> usageHistory;

  UsageList({required this.usageHistory});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: usageHistory.length,
      itemBuilder: (context, index) {
        final usage = usageHistory[index];
        return ListTile(
          title: Text("Usage #${usage.usageNum}"),
          subtitle: Text("Name: ${usage.name}\nStart: ${usage.startTime}\nEnd: ${usage.stopTime}\nDate: ${usage.usageDate}"),
        );
      },
    );
  }
}
