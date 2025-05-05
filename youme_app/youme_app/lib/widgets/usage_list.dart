import 'package:flutter/material.dart';
import 'package:youme_app/models/usage_history.dart';
import 'package:intl/intl.dart';

class UsageList extends StatelessWidget {
  final List<UsageHistory> usageHistoryList;
  final DateFormat datetimeFormat = DateFormat('yyyy-MM-dd HH:mm:ss');
  final DateFormat dateFormat = DateFormat('yyyy-MM-dd');

  UsageList({required this.usageHistoryList});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: usageHistoryList.length,
      itemBuilder: (context, index) {
        final usage = usageHistoryList[index];

        String startTimeStr = usage.startTime != null ? datetimeFormat.format(usage.startTime!) : 'N/A';
        String stopTimeStr = usage.stopTime != null ? datetimeFormat.format(usage.stopTime!) : 'N/A';
        String usageDateStr = usage.usageDate != null ? dateFormat.format(usage.usageDate!) : 'N/A';

        return Card(
          margin: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          elevation: 3,
          child: ListTile(
            title: Text("Usage #${usage.usageNum} - ${usage.name}"),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(height: 4),
                Text("Start: $startTimeStr"),
                Text("End: $stopTimeStr"),
                Text("Date: $usageDateStr"),
              ],
            ),
          ),
        );
      },
    );
  }
}
