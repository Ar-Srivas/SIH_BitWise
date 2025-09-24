//
//  ContentView.swift
//  Demo project
//
//  Created by Divy Pashine on 11/09/25.
//

import SwiftUI
import UIKit
import AVFoundation
import FirebaseCore
import FirebaseFirestore
import KeychainAccess
struct ContentView: View {
    @State private var username=""
    @State private var password=""
    @State private var isloggedin=false
    @State private var showpass=false
    @State private var wrongcred=false
    @State private var emptynameorpass=false
    @State private var usernotfound=false
    @State private var wrongdevice=false
    @State private var deviceregistered=false
    let db=Firestore.firestore()
    var body: some View {
        NavigationStack{
            ZStack{
                LinearGradient(
                    colors: [Color.black.opacity(30), Color.gray.opacity(0.6)],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                                .ignoresSafeArea()
                VStack{
                    Image("Image").resizable().scaledToFit().frame(width: 100,height: 100)
                    Spacer().frame(height: 50)
                    TextField("Username",text: $username).padding().foregroundColor(Color.myasset).textFieldStyle(RoundedBorderTextFieldStyle()).frame(width: 300, height: 50).autocorrectionDisabled().textInputAutocapitalization(.never)
                        .overlay(RoundedRectangle(cornerRadius: 8).stroke(wrongcred || emptynameorpass ? Color.red : Color.black, lineWidth: 3).frame(width: 270,height: 35))
                    if showpass{
                        TextField("Passowrd",text: $password).padding().frame(width: 300, height: 50).foregroundColor(Color.myasset).textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocorrectionDisabled().textInputAutocapitalization(.never)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(wrongcred || emptynameorpass ? Color.red : Color.black, lineWidth: 3).frame(width: 270,height: 35))
                    }
                    else{
                        SecureField("Passowrd",text: $password).padding().frame(width: 300, height: 50).foregroundColor(Color.myasset).textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocorrectionDisabled().textInputAutocapitalization(.never)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(wrongcred || emptynameorpass ? Color.red : Color.black, lineWidth: 3).frame(width: 270,height: 35))
                    }
                    if (!wrongcred && !usernotfound && !emptynameorpass){
                        Text("Enter Credentials").foregroundColor(Color.white)
                    }
                    if (wrongcred){
                        Text("Wrong Username or password").foregroundColor(Color.red).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ wrongcred = false}
                        }
                    }
                    if (usernotfound){
                        Text("User Not found").foregroundColor(Color.red).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ usernotfound = false}
                        }
                    }
                    if (emptynameorpass){
                        Text("Please Enter Your Credentials").foregroundColor(Color.red).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ emptynameorpass = false}
                        }
                    }
                    if (wrongdevice){
                        Text("This is not your registered device").foregroundColor(Color.red).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ wrongdevice = false}
                        }
                    }
                    Toggle(isOn: $showpass) {
                        Text("Show Password").padding().foregroundColor(Color.white)
                    }.padding().frame(minWidth: 10,minHeight: 80).tint(Color.mycolor)
                    
                    Button(action: {
                        if (username=="" && password==""){
                            emptynameorpass=true
                            return
                        }
                        checkPassword(username: username, password: password)
                    }) {
                        HStack {
                            Text("Login")
                        }
                        .foregroundColor(.black)
                    }
                    .padding()
                    .background(Color.mycolor)
                    .cornerRadius(25)
                }.padding().foregroundColor(Color.blue).cornerRadius(65)
                
            }.navigationDestination(isPresented: $isloggedin) { Mainpage(username:username,deviceregistered: deviceregistered)}
                .hideKeyboardOnTap()
            
        }.navigationBarHidden(true)
    }
    func checkPassword(username: String, password: String) {
        let db = Firestore.firestore()
        let deviceUUID = PersistentDeviceUUID.get()
        print("Device ID: \(deviceUUID)")
        
        let docRef = db.collection("students").document(username)
        docRef.getDocument { (document, error) in
            if let error = error {
                print("Error fetching document: \(error)")
                return
            }
            if let document=document, document.exists{
                let data=document.data()
                let dbpassword=data?["password"] as? String?
                let deviceid=data?["deviceid"] as? String?
                if (deviceid==deviceUUID){
                    if (dbpassword==password){
                        isloggedin.toggle()
                    }
                    else{
                        wrongcred=true
                        print("Wrong Credentials")
                    }
                }else if (deviceid==""){
                    docRef.updateData(["deviceid":deviceUUID])
                    deviceregistered=true
                    if (dbpassword==password){
                        isloggedin.toggle()
                    }
                    else{
                        wrongcred=true
                        print("Wrong Credentials")
                    }
                }
                else{
                    wrongdevice=true
                    return
                }
            }
            else{
                print("User Not Found")
                usernotfound=true
                
            }
        }
    }
}

struct Mainpage: View {
    @Environment(\.dismiss) var dismiss
    @State private var showqrpage=false
    @State private var currenttime=Date()
    @State private var useractualname=""
    @State private var changepassword=false
    var username:String
    var deviceregistered:Bool
    var body: some View {
        NavigationStack{
            ZStack{
                
                LinearGradient(
                    colors: [Color.black.opacity(30), Color.gray.opacity(0.6)],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                                .ignoresSafeArea()
                VStack{
                    if(deviceregistered){
                        Text("Your Device was Registered for the first time").foregroundColor(Color.mycolor)
                        }
                    Text(currenttime.formatted(date: .numeric, time: .standard)).foregroundColor(Color.white).onAppear{
                        Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true){ Timer in
                            currenttime=Date()
                        }}.frame(maxWidth: .infinity,alignment: .trailing).padding()
                    Spacer().frame(height: 170)
                    VStack{
                        Text("Logged In as:")
                            .foregroundColor(.white.opacity(0.8))
                            .font(.subheadline)
                        
                        Text(username)
                            .foregroundColor(.white)
                            .font(.title2.bold())
                        
                        Text("Name")
                            .foregroundColor(.white.opacity(0.7))
                            .font(.subheadline)
                            .frame(width: 100, height: 20)
                        
                        Text(useractualname)
                            .foregroundColor(.white)
                            .font(.headline)
                            .frame(width: 140, height: 24)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(
                                RoundedRectangle(cornerRadius: 12)
                                    .fill(Color.white.opacity(0.1)))
                    } .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 20)
                                .fill(Color.white.opacity(0.05))
                                .shadow(color: .black.opacity(0.4), radius: 6, x: 0, y: 4))
                    Spacer()
                    HStack{
                        Button(action: {showqrpage.toggle()}){
                            Image(systemName: "qrcode").resizable().frame(width: 50,height: 50).foregroundColor(Color.white)
                        }.frame(height: .infinity,alignment: .leading)
                        Spacer().frame(width: 50,height: 50)
                        Button(action: {}){
                            Image(systemName: "person.crop.circle.fill").resizable().frame(width: 50,height: 50).foregroundColor(Color.mycolor).disabled(true)
                        }.frame(height: .infinity,alignment: .trailing)
                    }
                }
                .navigationDestination(isPresented: $showqrpage){
                    qrpage(username: username,useractualname: useractualname)
                }
                .navigationDestination(isPresented: $changepassword){
                            changepass(username: username, useractualname: useractualname)
                        }
            }.navigationBarBackButtonHidden(true)
                .onAppear {
                    getname(inputusername: username)
                }
                .toolbar {
                    ToolbarItem(placement: .principal) {
                        Text("Attendance App")
                            .font(.title2.bold())
                            .foregroundColor(Color.mycolor)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(
                                RoundedRectangle(cornerRadius: 30)
                                    .stroke(Color.white, lineWidth: 1)
                            )
                            .padding(.top, 4)
                    }
                    ToolbarItem(placement: .topBarTrailing) {
                        Menu {
                            NavigationLink("Change Password") {
                                changepass(username: username, useractualname: useractualname)
                            }
                            Button("Logout") {
                                dismiss()
                            }
                        } label: {
                            Image(systemName: "ellipsis.circle")
                                .font(.title2)
                                .foregroundColor(Color.mycolor)
                        }
                    }
                }
        }
    }
    
    func getname(inputusername:String){
        let db = Firestore.firestore()
        
        let docRef = db.collection("students").document(inputusername)
        docRef.getDocument { (document, error) in
            if let error = error {
                print("Error fetching document: \(error)")
                return
            }
            if let document=document, document.exists{
                let data=document.data()
                let name=data?["name"] as? String?
                useractualname=(name ?? "Server Error")!
            }
            else{
                print("User Not Found")
            }
        }
    }
}

struct changepass: View {
    var username:String
    var useractualname:String
    @Environment(\.dismiss) var dismiss
    @State private var currentpassword=""
    @State private var newpassword=""
    @State private var confirmnewpassword=""
    @State private var wrongcurrentpassword=false
    @State private var passwordnotmatching=false
    @State private var enterallfeilds=false
    @State private var passwordchangedsuccess=false
    @State private var showmainpageagain=false
    @State private var cannotchange=false
    @State private var somethingwentwrong=false
    var body: some View {
        NavigationStack{
            ZStack{
                LinearGradient(
                    colors: [Color.black.opacity(30), Color.gray.opacity(0.6)],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                                .ignoresSafeArea()
                VStack{
                    Text("Username: \(username)").foregroundColor(.white)
                    TextField("Enter Current Password",text: $currentpassword).padding()
                        .foregroundColor(Color.myasset).frame(width: 400, height: 50).textFieldStyle(RoundedBorderTextFieldStyle()).autocorrectionDisabled().textInputAutocapitalization(.never)
                        .overlay(RoundedRectangle(cornerRadius : 8).stroke(wrongcurrentpassword || enterallfeilds ? Color.red : Color.black, lineWidth: 3).frame(maxWidth: 370,maxHeight: 36))
                    TextField("Enter New Password",text: $newpassword).padding().foregroundColor(Color.myasset).frame(width: 400, height: 50).textFieldStyle(RoundedBorderTextFieldStyle()).autocorrectionDisabled().textInputAutocapitalization(.never)
                        .overlay(RoundedRectangle(cornerRadius : 8).stroke(passwordnotmatching || enterallfeilds ? Color.red : Color.black, lineWidth: 3).frame(maxWidth: 370,maxHeight: 36))
                    TextField("Confirm Password",text: $confirmnewpassword).padding().foregroundColor(Color.myasset).frame(width: 400, height: 50).textFieldStyle(RoundedBorderTextFieldStyle()).autocorrectionDisabled().textInputAutocapitalization(.never)
                        .overlay(RoundedRectangle(cornerRadius : 8).stroke(passwordnotmatching || enterallfeilds ? Color.red : Color.black, lineWidth: 3).frame(maxWidth: 370,maxHeight: 36))
                    if (cannotchange){
                        Text("Enter a different password").foregroundColor(Color.mycolor).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ cannotchange = false}
                        }
                    }
                    if (!wrongcurrentpassword && !passwordnotmatching){
                        Text("Enter Credentials").foregroundColor(Color.white)
                    }
                    if (wrongcurrentpassword){
                        Text("Wrong Current Password").foregroundColor(Color.mycolor).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ wrongcurrentpassword = false}
                        }
                    }
                    if (passwordnotmatching){
                        Text("Your passwords do not match").foregroundColor(Color.mycolor).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ passwordnotmatching = false}
                        }
                    }
                    if (enterallfeilds){
                        Text("All feild are mandatory").foregroundColor(Color.mycolor).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ enterallfeilds = false}
                            
                        }}
                    if (passwordchangedsuccess){
                        Text("Password Changed Successfully").foregroundColor(Color.green).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ passwordchangedsuccess = false}
                        }
                    }
                    if (somethingwentwrong){
                        Text("Something Went Wrong, Please try again later or Re-login").foregroundColor(Color.mycolor).onAppear{
                            DispatchQueue.main.asyncAfter(deadline: .now() + 2){ somethingwentwrong = false}
                        }
                    }
                    Button(action: {
                        if (currentpassword=="" || newpassword=="" || confirmnewpassword==""){
                            enterallfeilds=true
                            return
                        }
                        if (newpassword==confirmnewpassword){
                            setnewpassword(username: username, currentpassword: currentpassword, newpassword: newpassword, confirmpassword: confirmnewpassword)
                        }
                        else{
                            passwordnotmatching=true
                            return
                        }
                        setnewpassword(username: username, currentpassword: currentpassword, newpassword: newpassword, confirmpassword: confirmnewpassword)
                    }){
                        HStack{
                            Text("Confirm")
                        }.padding().foregroundColor(Color.black).background(Color.mycolor).cornerRadius(40)
                    }
                }
            }.navigationBarBackButtonHidden(false).hideKeyboardOnTap()
                }
            }
        
        
    
    func setnewpassword(username:String,currentpassword:String,newpassword:String,confirmpassword:String){
        let db=Firestore.firestore()
        let docref=db.collection("students").document(username)
        docref.getDocument{ (document, error) in
            if let error = error{
                print("Error Fetching \(error)")
            }
            if let document=document, document.exists{
                let data=document.data()
                let dbpassword=data?["password"] as? String?
                if(dbpassword==currentpassword){
                    if (currentpassword==newpassword && currentpassword==confirmnewpassword){
                        cannotchange=true
                        return
                    }
                    docref.updateData(["password": confirmpassword]) { err in
                        if let err = err {
                            print("Error updating: \(err)")
                        } else {
                            print("Attendance marked!")
                            passwordchangedsuccess = true
                        }
                    }
                }
                else{
                    wrongcurrentpassword=true
                    return
                }
            }else{
                print("UsernotFound")
                somethingwentwrong=true
            }
        }
    }
}

struct qrpage: View {
    var username:String
    @State private var showMainpage=false
    var useractualname:String
    @State var rawdata=""
    @State private var currenttime=Date()
    @State var cameranotfoundorpermissiondenied=false
    @State private var attendancemarked=false
    @State private var invalidqrcode=false
    @State private var unknownerror=false
    @State private var looseinternet=false
    @State private var studentnotfound=false
    @State private var documentnotfound=false
    @State private var issessionactive=true
    var body: some View {
        NavigationStack {
            ZStack {
                LinearGradient(
                    colors: [Color.black.opacity(30), Color.gray.opacity(0.6)],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                                .ignoresSafeArea()
                VStack {
                    VStack {
                        Text("Marking Attendance for:")
                            .foregroundColor(.white)
                        Text(username)
                            .foregroundColor(.white)
                        Text(currenttime.formatted(date: .numeric, time: .standard)).foregroundColor(Color.white).onAppear{
                            Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true){ Timer in
                                currenttime=Date()
                            }}.frame(maxWidth: .infinity,alignment: .trailing).padding()
                    }
                    .frame(maxHeight: .infinity, alignment: .top)
                    QRScannerView { code in
                        if code == "NO_CAMERA" || code == "CAMERA_ERROR" {
                            cameranotfoundorpermissiondenied = true
                        } else {
                            self.rawdata = code
                            if !attendancemarked {
                                markattendance(qrdata: rawdata)
                            }
                        }
                    }
                    .frame(width: 350, height: 350)
                    .cornerRadius(12)
                    .clipped()
                    .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.white,lineWidth: 2))
                    VStack {
                        if attendancemarked {
                            Text("Attendance Marked Successfully")
                                .foregroundColor(.green)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                        attendancemarked = false
                                    }
                                }
                        }
                        if invalidqrcode {
                            Text("Invalid QR Code")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                                        invalidqrcode = false
                                    }
                                }
                        }
                        if unknownerror {
                            Text("An Error Occurred")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                                        unknownerror = false
                                    }
                                }
                        }
                        if studentnotfound {
                            Text("Student Not Found, ask your faculty to add you")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                        studentnotfound = false
                                    }
                                }
                        }
                        if documentnotfound {
                            Text("Invalid QR Code")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                        documentnotfound = false
                                    }
                                }
                        }
                        if looseinternet {
                            Text("Unable to Connect to Database, Check your connection")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                                        looseinternet = false
                                    }
                                }
                        }
                        if cameranotfoundorpermissiondenied {
                            Text("There was an issue connecting to the camera or permission was not provided")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                        cameranotfoundorpermissiondenied = false
                                    }
                                }
                        }
                        if !issessionactive{
                            Text("The Session is no longer active, ask your faculty to activate to mark your attendance")
                                .foregroundColor(Color.mycolor)
                                .font(.title3)
                                .onAppear {
                                    DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                        issessionactive = true
                                    }
                                }
                        }
                    }
                    Spacer().frame(height: 200)
                    HStack {
                        Button(action: {}) {
                            Image(systemName: "qrcode")
                                .resizable()
                                .frame(width: 50, height: 50)
                                .foregroundColor(Color.mycolor)
                        }
                        .disabled(true)
                        
                        Spacer().frame(width: 50)
                        
                        Button(action: { showMainpage.toggle() }) {
                            Image(systemName: "person.crop.circle.fill")
                                .resizable()
                                .frame(width: 50, height: 50)
                                .foregroundColor(.white)
                        }
                    }
                }
            }
            .navigationDestination(isPresented: $showMainpage) {
                Mainpage(username: username,deviceregistered: false)
            }
            .toolbar(.hidden, for: .navigationBar)
        }
    }
    func markattendance(qrdata: String) {
        let db = Firestore.firestore()
        let currenttime = Date()
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd"
        let dateString = dateFormatter.string(from: currenttime)
        //check this part
        let splitdata=qrdata.split(separator: "#")
        if (splitdata.count > 2){
            invalidqrcode=true
            return
        }
        let teacherinfo=splitdata[0]
        //
        
        let invalidCharacters = CharacterSet(charactersIn: "/[]?")
        if qrdata.trimmingCharacters(in: .whitespaces).isEmpty || qrdata.rangeOfCharacter(from: invalidCharacters) != nil {
            print("Invalid QR code for Firestore path!")
            invalidqrcode = true
            return
        }
        
        let docRef = db.collection("teachers")
            .document(String(teacherinfo))
            .collection("attendance_records")
            .document(dateString)
        
        docRef.getDocument { (document, error) in
            if let error = error {
                print("Firestore error: \(error.localizedDescription)")
                looseinternet = true
                return
            }
            
            guard let document = document, document.exists else {
                documentnotfound = true
                return
            }
            
            let data = document.data() ?? [:]
            let sessionactive=data["is_session_active"] as? Bool?
            let qrvalue=data["qrvalue"] as? String?
            if (sessionactive==false){
                issessionactive=false
                return
            }
            if (qrvalue==qrdata){
                var students = data["students"] as? [String: [String: Any]] ?? [:]
                
                guard var studentData = students[self.username] else {
                    studentnotfound = true
                    return
                }
                let time = Timestamp(date: Date())
                studentData["status"] = "present"
                studentData["timestamp"] = time
                students[self.username] = studentData
                
                docRef.updateData(["students": students]) { err in
                    if let err = err {
                        print("Error updating: \(err.localizedDescription)")
                        looseinternet = true
                    } else {
                        attendancemarked = true
                    }
                }
            }
            else{
                invalidqrcode=true
                return
            }
        }
    }
}

struct QRScannerView: UIViewControllerRepresentable {
    var onCodeScanned: ((String) -> Void)?
    func makeUIViewController(context: Context) -> initializeQRScanner {
        let controller = initializeQRScanner()
        controller.onCodeScanned = onCodeScanned
        return controller
    }
    
    func updateUIViewController(_ uiViewController: initializeQRScanner, context: Context) {}
}

class initializeQRScanner:UIViewController {
    
    let captureSession = AVCaptureSession()
    var videopreviewlayer:AVCaptureVideoPreviewLayer?
    var onCodeScanned: ((String) -> Void)?
    override func viewDidLoad() {
        print("Starting camera setup…")
        super.viewDidLoad()
        view.backgroundColor = .black
        initializeqrscanner()
    }
    private func initializeqrscanner(){
        guard let captureDevice = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            print("No camera available")
            onCodeScanned?("NO_CAMERA")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice)
            if captureSession.canAddInput(input) {
                captureSession.addInput(input)
            }
            
            let metadataOutput = AVCaptureMetadataOutput()
            if captureSession.canAddOutput(metadataOutput) {
                captureSession.addOutput(metadataOutput)
                
                metadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
                metadataOutput.metadataObjectTypes = [.qr]
            }
            
            let videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
            videoPreviewLayer.videoGravity = .resizeAspectFill
            videoPreviewLayer.frame = view.layer.bounds
            view.layer.addSublayer(videoPreviewLayer)
            
            captureSession.startRunning()
            
        } catch {
            print("Error setting up camera: \(error)")
            onCodeScanned?("CAMERA_ERROR")
            return
        }
    }
}
extension initializeQRScanner:AVCaptureMetadataOutputObjectsDelegate{
    func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput
                        metadataObjects: [AVMetadataObject], from connection:
                        AVCaptureConnection) {
        if let obj = metadataObjects.first as? AVMetadataMachineReadableCodeObject,
           obj.type == .qr,
           let code = obj.stringValue {
            print("Code: \(code)")
            onCodeScanned?(code)
        }
    }
}
extension View {
    func hideKeyboardOnTap() -> some View {
        self.onTapGesture {
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
    }
}

#Preview {
    //ContentView()
    //Mainpage(username: "Def", deviceregistered: true)
    qrpage(username: "Def",useractualname: "def")
    //changepass(username: "def@ex", useractualname: "def")
}
import Foundation
import Security

final class PersistentDeviceUUID {
    private static let key = "divy.Attendance.app"

    static func get() -> String {
        if let existingUUID = loadFromKeychain() {
            return existingUUID
        }
        let newUUID = UUID().uuidString
        saveToKeychain(uuid: newUUID)
        return newUUID
    }
    private static func loadFromKeychain() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: kCFBooleanTrue!,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var dataTypeRef: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &dataTypeRef)
        guard status == errSecSuccess,
              let retrievedData = dataTypeRef as? Data,
              let uuid = String(data: retrievedData, encoding: .utf8) else {
            return nil
        }
        return uuid
    }
    private static func saveToKeychain(uuid: String) {
        guard let data = uuid.data(using: .utf8) else { return }
        let deleteQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        SecItemDelete(deleteQuery as CFDictionary)
        let addQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        SecItemAdd(addQuery as CFDictionary, nil)
    }
}
