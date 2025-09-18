package com.example.attapp;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextClock;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.widget.Toolbar;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import java.sql.Time;
import java.util.Calendar;


public class mainpage extends AppCompatActivity {

    private TextView main_username, main_name;
    private ImageButton qr;
    private Toolbar toolbar;
    TextClock time;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mainpage);

        String username = getIntent().getStringExtra("username");
        String name = getIntent().getStringExtra("name");

        main_username = findViewById(R.id.mainusername);
        main_name = findViewById(R.id.main_name);
        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        time=findViewById(R.id.time);
        getSupportActionBar().setDisplayShowTitleEnabled(true);
        getSupportActionBar().setTitle("Attendance App");

        qr = findViewById(R.id.main_qr);

        main_username.setText(username);
        main_name.setText(name);

        time.setTimeZone("Asia/Kolkata");
        time.setFormat12Hour("dd/MM/yyyy hh:mm:ss");


        qr.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(mainpage.this, qrpage.class);
                intent.putExtra("username", username);
                intent.putExtra("name", name);
                startActivity(intent);
                finish();
                overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            }
        });
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.logout) {
            finish();
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            Toast.makeText(this, "Logged Out", Toast.LENGTH_SHORT).show();
            return true;
        } else if (item.getItemId()==R.id.changepass) {
            Intent intent=new Intent(mainpage.this,changepass.class);
            intent.putExtra("username",main_username.getText().toString());
            startActivity(intent);
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
    @SuppressLint("GestureBackNavigation")
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Toast.makeText(mainpage.this,"Logged Out",Toast.LENGTH_SHORT).show();
    }

}
