from ultralytics import YOLO

if __name__ == '__main__':
    
    # Load a pre-trained base model
    model = YOLO("yolov8s.pt")
    
    # Train the model with the new dataset
    model.train(
        data="TrashNet- A set of annotated images of trash that can be used for object detection.v20i.yolov8/data.yaml",
        epochs=50,
        imgsz=640,
        project="runs",          # Saves to d:\Garbage_Sorting_AI\runs
        name="garbage_model"     # The folder inside runs will be named garbage_model
    )
    
    print("Training successfully completed!")