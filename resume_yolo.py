from ultralytics import YOLO

if __name__ == '__main__':
    # Load the last saved weights
    model = YOLO(r"C:\Users\MSI\runs\detect\runs\garbage_model\weights\last.pt")
    
    # Resume training from epoch 41
    model.train(resume=True)
    
    print("Training successfully resumed and completed!")
