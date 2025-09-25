package com.example.attapp;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.Image;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextClock;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.google.common.util.concurrent.ListenableFuture;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.mlkit.vision.barcode.BarcodeScanner;
import com.google.mlkit.vision.barcode.BarcodeScanning;
import com.google.mlkit.vision.barcode.common.Barcode;
import com.google.mlkit.vision.common.InputImage;

import java.time.LocalDate;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.Executors;

public class qrpage extends AppCompatActivity {
    private PreviewView previewView;
    private ImageButton mainpage;
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 1001;
    private TextView qr_username;
    private boolean qrProcessed = false;
    TextClock time;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_qrpage);

        previewView = findViewById(R.id.previewView);
        mainpage = findViewById(R.id.mainpage);
        qr_username=findViewById(R.id.qr_name);
        time=findViewById(R.id.time);
        time.setTimeZone("Asia/Kolkata");
        time.setFormat12Hour("dd/MM/yyyy hh:mm:ss a");

        String username = getIntent().getStringExtra("username");
        String name = getIntent().getStringExtra("name");

        qr_username.setText(username);


        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
        } else {
            startCamera(username,name);
        }

        mainpage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(qrpage.this,mainpage.class);
                intent.putExtra("username",username);
                intent.putExtra("name", name);
                startActivity(intent);
                finish();
                overridePendingTransition(android.R.anim.slide_in_left, android.R.anim.slide_out_right);
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                String username = getIntent().getStringExtra("username");
                String name = getIntent().getStringExtra("name");
                startCamera(username,name);
            } else {
                Log.e("QR", "Camera permission denied");
            }
        }
    }
    @SuppressLint("GestureBackNavigation")
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Toast.makeText(qrpage.this,"Logged Out",Toast.LENGTH_SHORT).show();
    }

    private void startCamera(String username,String name) {
        if (previewView == null) {
            Log.e("QR", "PreviewView is null in startCamera.");
            return;
        }

        ListenableFuture<ProcessCameraProvider> cameraProviderFuture =
                ProcessCameraProvider.getInstance(this);

        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();

                Preview preview = new Preview.Builder().build();
                if (previewView.getDisplay() == null) {
                    previewView.post(() -> {
                        if (previewView.getDisplay() != null) {
                            preview.setSurfaceProvider(previewView.getSurfaceProvider());
                        }
                    });
                } else {
                    preview.setSurfaceProvider(previewView.getSurfaceProvider());
                }

                ImageAnalysis imageAnalysis = new ImageAnalysis.Builder()
                        .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                        .build();

                imageAnalysis.setAnalyzer(Executors.newSingleThreadExecutor(), image -> {
                    @SuppressLint("UnsafeOptInUsageError")
                    Image mediaImage = image.getImage();
                    if (mediaImage != null) {
                        InputImage inputImage = InputImage.fromMediaImage(
                                mediaImage, image.getImageInfo().getRotationDegrees());

                        BarcodeScanner scanner = BarcodeScanning.getClient();
                        scanner.process(inputImage)
                                .addOnSuccessListener(barcodes -> {
                                    for (Barcode barcode : barcodes) {
                                        handleBarcode(barcode.getRawValue(), username,name);
                                    }
                                })
                                .addOnFailureListener(e -> Log.e("QR", "Barcode scanning error", e))
                                .addOnCompleteListener(task -> image.close());
                    } else {
                        image.close();
                    }
                });

                CameraSelector cameraSelector = new CameraSelector.Builder()
                        .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                        .build();

                cameraProvider.unbindAll();
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageAnalysis);

            } catch (Exception e) {
                Log.e("QR", "Use case binding failed", e);
            }
        }, ContextCompat.getMainExecutor(this));
    }

    private void handleBarcode(String rawValue, String username,String name) {
        if (qrProcessed) return;

        qrProcessed = true;

        FirebaseFirestore db = FirebaseFirestore.getInstance();
        String[] stplitqr=rawValue.split("#");
        String teacherName = stplitqr[0];
        markAttendance(db, teacherName, username, rawValue);

        qrProcessed=true;
        previewView.postDelayed(() -> qrProcessed = false, 5000);
    }
    private void markAttendance(FirebaseFirestore db, String teacherName, String currentUsername, String rawQrData) {
        // Validate QR data
        if (rawQrData == null || rawQrData.isEmpty()) {
            Toast.makeText(this, "Invalid QR Code!", Toast.LENGTH_LONG).show();
            return;
        }

        String[] qrDataParts = rawQrData.split("#");
        if (qrDataParts.length > 2) {
            Toast.makeText(this, "Invalid QR Code!", Toast.LENGTH_LONG).show();
            return;
        }

        String qrTeacherName = qrDataParts[0];
        if (!Objects.equals(teacherName, qrTeacherName)) {
            Toast.makeText(this, "QR Code does not match teacher!", Toast.LENGTH_LONG).show();
            return;
        }

        // Get current date
        LocalDate date;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            date = LocalDate.now();
        } else {
            Toast.makeText(this, "Device not supported", Toast.LENGTH_LONG).show();
            return;
        }

        // Reference to attendance document
        DocumentReference docRef = db.collection("teachers")
                .document(teacherName)
                .collection("attendance_records")
                .document(String.valueOf(date));

        // Fetch document and update attendance
        docRef.get().addOnSuccessListener(snapshot -> {
            if (snapshot.exists()) {
                Boolean isSessionActive = snapshot.getBoolean("is_session_active");
                String qrValue = snapshot.getString("qrvalue");

                if (Boolean.TRUE.equals(isSessionActive)) {
                    if (Objects.equals(qrValue, rawQrData)) {
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
                                        .addOnSuccessListener(aVoid ->
                                                Toast.makeText(this, "Attendance marked!", Toast.LENGTH_LONG).show())
                                        .addOnFailureListener(e -> {
                                            Log.e("QR", "Error updating student", e);
                                            Toast.makeText(this, "Error marking attendance", Toast.LENGTH_LONG).show();
                                        });
                            } else {
                                Toast.makeText(this, "Student data missing!", Toast.LENGTH_LONG).show();
                            }
                        } else {
                            Toast.makeText(this, "Student not found in record!", Toast.LENGTH_LONG).show();
                        }
                    } else {
                        Toast.makeText(this, "Invalid QR Code!", Toast.LENGTH_LONG).show();
                    }
                } else {
                    Toast.makeText(this, "Session is no longer active", Toast.LENGTH_LONG).show();
                }
            } else {
                Toast.makeText(this, "Invalid QR Code!", Toast.LENGTH_LONG).show();
            }
        }).addOnFailureListener(e -> {
            Toast.makeText(this, "Error accessing database!", Toast.LENGTH_LONG).show();
            Log.e("QR", "Firestore error", e);
        });
    }

}
