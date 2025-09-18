package com.example.attapp;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.Image;
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
import com.google.mlkit.vision.barcode.BarcodeScanner;
import com.google.mlkit.vision.barcode.BarcodeScanning;
import com.google.mlkit.vision.barcode.common.Barcode;
import com.google.mlkit.vision.common.InputImage;

import java.util.Date;
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

        Intent intent = new Intent(this, givepresent.class);
        intent.putExtra("username", username);
        intent.putExtra("name",name);
        intent.putExtra("qrdata", rawValue);
        startActivity(intent);
        qrProcessed=true;
        previewView.postDelayed(() -> qrProcessed = false, 5000);
    }
}
