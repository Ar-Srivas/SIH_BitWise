//
//  Demo_projectApp.swift
//  Demo project
//
//  Created by Divy Pashine on 11/09/25.
//

import SwiftUI
import FirebaseCore
import FirebaseFirestore
@main
struct Demo_projectApp: App {
    init(){
        FirebaseApp.configure()
    }
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
