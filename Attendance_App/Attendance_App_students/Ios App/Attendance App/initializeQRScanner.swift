//
//  Untitled.swift
//  Demo project
//
//  Created by Divy Pashine on 12/09/25.
//
import UIKit
import AVFoundation
class initializeQRScanner:UIViewController {
    let captureSession = AVCaptureSession()
    var videopreviewlayer:AVCaptureVideoPreviewLayer?
    var onCodeScanned: ((String) -> Void)?
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    private func initializeqrscanner(){
        guard let captureDevice = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            print("No camera available")
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
