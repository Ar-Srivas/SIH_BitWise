package com.example.attapp;

import android.content.Intent;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.provider.Settings;
import android.text.InputType;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.material.color.DynamicColors;
import com.google.android.material.color.utilities.DynamicColor;
import com.google.firebase.Firebase;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.Objects;

public class MainActivity extends AppCompatActivity {
    private EditText un, pass;
    private Button login;
    private FirebaseFirestore db;
    CheckBox visibility;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        un=findViewById(R.id.username);
        pass=findViewById(R.id.password);
        pass.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        login=findViewById(R.id.userlogin);
        visibility=findViewById(R.id.visibility);
        db=FirebaseFirestore.getInstance();
        String androidid=Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
        Log.e("your id",androidid);
        visibility.setOnCheckedChangeListener((buttonView, isChecked) -> {
                    if (visibility.isChecked()){
                        pass.setInputType(InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
                        pass.setSelection(pass.getText().length());
                    } else {
                        pass.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
                        pass.setSelection(pass.getText().length());
                    }
        });
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username=un.getText().toString();
                String password=pass.getText().toString();
                if (username.isEmpty() || password.isEmpty()){
                    Toast.makeText(MainActivity.this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                    return;
                }
                db.collection("students").document(username).get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                    @Override
                    public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                        if (task.isSuccessful()){
                            DocumentSnapshot dc=task.getResult();
                            if (dc.exists()){
                                String dbPass=dc.getString("password");
                                String name=dc.getString("name");
                                String deviceid=dc.getString("deviceid");
                                if (deviceid.isBlank()){
                                    db.collection("students").document(username).update("deviceid",androidid);
                                }
                                else if (Objects.equals(deviceid, androidid)){
                                    Toast.makeText(MainActivity.this, "Your Device was registered for the first time", Toast.LENGTH_LONG).show();
                                if (Objects.equals(dbPass, password)){
                                        Toast.makeText(MainActivity.this, "Login Successful", Toast.LENGTH_SHORT).show();
                                        Intent intent=new Intent(MainActivity.this, mainpage.class);
                                        intent.putExtra("username",username);
                                        intent.putExtra("name",name);
                                        startActivity(intent);
                                        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
                                }
                                else {
                                    Toast.makeText(MainActivity.this, "Invalid Credentials", Toast.LENGTH_SHORT).show();
                                }
                            }else{
                                    Toast.makeText(MainActivity.this,"This is not your registered Device",Toast.LENGTH_LONG).show();
                                }
                            }
                                else {
                                Toast.makeText(MainActivity.this,
                                        "Invalid Credentials",
                                        Toast.LENGTH_SHORT).show();
                            }
                        } else {
                            Toast.makeText(MainActivity.this,
                                    "Error: " + task.getException().getMessage(),
                                    Toast.LENGTH_SHORT).show();
                            }
                        }
                });
            }
        });
    }




}