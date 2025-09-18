package com.example.attapp;

import android.content.Intent;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;

public class changepass extends AppCompatActivity {
    EditText currentpass, newpass, confirmpass;
    TextView username;
    Button confirm;
    ImageButton back;
    CheckBox visibility;
    private FirebaseFirestore db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_changepass);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        db = FirebaseFirestore.getInstance();
        currentpass = findViewById(R.id.currentpassword);
        newpass = findViewById(R.id.newpassword);
        confirmpass = findViewById(R.id.confirmpassword);
        username = findViewById(R.id.change_username);
        confirm = findViewById(R.id.confirm);
        back = findViewById(R.id.back);
        visibility = findViewById(R.id.visibility);
        newpass.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        confirmpass.setInputType(InputType.TYPE_CLASS_TEXT| InputType.TYPE_TEXT_VARIATION_PASSWORD);

        String name = getIntent().getStringExtra("username");
        username.setText(name);

        visibility.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (visibility.isChecked()){
                newpass.setInputType(InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
                newpass.setSelection(newpass.getText().length());
                confirmpass.setInputType(InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
                confirmpass.setSelection(confirmpass.getText().length());
            } else {
                newpass.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                newpass.setSelection(newpass.getText().length());
                confirmpass.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                confirmpass.setSelection(confirmpass.getText().length());
            }
        });
        confirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String current = currentpass.getText().toString().trim();
                String newp = newpass.getText().toString().trim();
                String confirmP = confirmpass.getText().toString().trim();

                if (current.isEmpty() || newp.isEmpty() || confirmP.isEmpty()) {
                    Toast.makeText(changepass.this, "All fields are required", Toast.LENGTH_SHORT).show();
                    return;
                }

                if (!newp.equals(confirmP)) {
                    Toast.makeText(changepass.this, "New password and confirm password do not match", Toast.LENGTH_SHORT).show();
                    return;
                }

                DocumentReference userRef = db.collection("users").document(name);
                userRef.get().addOnSuccessListener(document -> {
                    if (document.exists()) {
                        String storedPassword = document.getString("password");

                        if (storedPassword != null && storedPassword.equals(current)) {
                            userRef.update("password", newp)
                                    .addOnSuccessListener(aVoid -> {
                                        Toast.makeText(changepass.this, "Password updated successfully", Toast.LENGTH_SHORT).show();
                                        finish();
                                    })
                                    .addOnFailureListener(e -> {
                                        Toast.makeText(changepass.this, "Failed to update password", Toast.LENGTH_SHORT).show();
                                    });
                        } else {
                            Toast.makeText(changepass.this, "Current password is incorrect", Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        Toast.makeText(changepass.this, "User not found", Toast.LENGTH_SHORT).show();
                    }
                }).addOnFailureListener(e -> {
                    Toast.makeText(changepass.this, "Error: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                });
            }
        });
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
                overridePendingTransition(android.R.anim.slide_in_left, android.R.anim.slide_out_right);
            }
        });
    }
}
