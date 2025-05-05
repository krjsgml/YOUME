import 'package:flutter/material.dart';
import 'package:youme_app/api/api_service.dart';
import 'package:youme_app/models/usage_history.dart';
import 'package:youme_app/widgets/usage_list.dart';

class UsageScreen extends StatefulWidget {
  @override
  _UsageScreenState createState() => _UsageScreenState();
}

class _UsageScreenState extends State<UsageScreen> {
  late Future<List<UsageHistory>> usageHistory;

  @override
  void initState() {
    super.initState();
    usageHistory = ApiService().fetchUsageHistories();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Usage History"),
      ),
      body: FutureBuilder<List<UsageHistory>>(
        future: usageHistory,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No usage records found"));
          } else {
            // 데이터를 역순으로 표시하기 위해 reversed 사용
            List<UsageHistory> reversedList = snapshot.data!.reversed.toList();
            return UsageList(usageHistoryList: reversedList);
          }
        },
      ),
    );
  }
}
