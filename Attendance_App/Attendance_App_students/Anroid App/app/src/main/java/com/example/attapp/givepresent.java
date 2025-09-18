package com.example.attapp;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;

import java.time.LocalDate;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class givepresent extends AppCompatActivity {
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LocalDate date;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            date = LocalDate.now();
        } else {
            date = null;
        }

        FirebaseFirestore db = FirebaseFirestore.getInstance();
        String currentUsername = getIntent().getStringExtra("username");
        String name = getIntent().getStringExtra("name");
        String rawqrdata = getIntent().getStringExtra("qrdata");

        if (rawqrdata == null || rawqrdata.isEmpty()) {
            Toast.makeText(this, "Invalid Qr Code!", Toast.LENGTH_LONG).show();
            finish();
            return;
        }
        String[] qrdata = rawqrdata.split("#");
        if (qrdata.length>2) {
            Toast.makeText(this, "Invalid Qr Code!", Toast.LENGTH_LONG).show();
            finish();
            return;
        }

        String teachername = qrdata[0];

        if (currentUsername == null || currentUsername.isEmpty()) {
            Log.e("QR", "Username is null or empty!");
            finish();
            return;
        }
        markAttendance(db, teachername, date, currentUsername,rawqrdata);
    }

    private void markAttendance(FirebaseFirestore db, String teachername, LocalDate date, String currentUsername,String qrdata) {
        if (date == null) {
            Toast.makeText(this, "Device not supported", Toast.LENGTH_LONG).show();
            return;
        }

        DocumentReference docRef = db.collection("teachers")
                .document(teachername)
                .collection("attendance_records")
                .document(String.valueOf(date));

        docRef.get().addOnSuccessListener(snapshot -> {
            if (snapshot.exists()) {
                Boolean issessionactive = snapshot.getBoolean("is_session_active");
                String qrvalue = snapshot.getString("qrvalue");
                if (Boolean.TRUE.equals(issessionactive)) {
                    if (Objects.equals(qrvalue, qrdata)) {
                        Map<String, Object> students = (Map<String, Object>) snapshot.get("students");

                        if (students != null && students.containsKey(currentUsername)) {
                            Map<String, Object> studentData = (Map<String, Object>) students.get(currentUsername);

                            if (studentData != null) {
                                Date time = Calendar.getInstance().getTime();
                                studentData.put("status", "present");
                                studentData.put("timestamp", time);
                                students.put(currentUsername, studentData);

                                Map<String, Object> updates = new HashMap<>();
                                updates.put("students", students);

                                docRef.update(updates)
                                        .addOnSuccessListener(aVoid -> {
                                            Toast.makeText(this, "Attendance marked!", Toast.LENGTH_LONG).show();
                                            finish();
                                        })
                                        .addOnFailureListener(e -> {
                                            Log.e("QR", "Error updating student", e);
                                            Toast.makeText(this, "Error marking attendance", Toast.LENGTH_LONG).show();
                                            finish();
                                        });
                            } else {
                                Toast.makeText(this, "Student not found in record!", Toast.LENGTH_LONG).show();
                                finish();
                            }
                        } else {
                            Toast.makeText(this, "Student not found in record!", Toast.LENGTH_LONG).show();
                            finish();
                        }
                    } else {
                        Toast.makeText(this, "Invalid Qr Code!", Toast.LENGTH_LONG).show();
                        finish();
                    }
                } else {
                    Toast.makeText(this, "Session Is No Longer Active", Toast.LENGTH_LONG).show();
                    finish();
                }
            }
            else {
                Toast.makeText(this, "Invalid Qr Code!", Toast.LENGTH_LONG).show();
                finish();
            }
        }).addOnFailureListener(e -> {
            Toast.makeText(this, "Invalid Qr Code!", Toast.LENGTH_LONG).show();
            finish();
        });
    }
}
