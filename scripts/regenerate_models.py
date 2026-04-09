
import os
import logging
from pathlib import Path
import joblib

from src.data_loading.adult import load_adult
from src.models.rf_trainer import RandomForestTrainer
from src.models.xgboost_trainer import XGBoostTrainer
from src.models.sklearn_trainers import SVMTrainer, MLPTrainer, LogisticRegressionTrainer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def regenerate_all_models():
    # 1. Setup paths
    base_dir = Path("experiments/exp1_adult/models")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Load data
    logger.info("Loading Adult dataset...")
    # load_adult returns (X_train, X_test, y_train, y_test, feature_names, preprocessor)
    data = load_adult()
    X_train, X_test, y_train, y_test = data[0], data[1], data[2], data[3]
    feature_names = data[4]
    preprocessor = data[5]
    
    # Save preprocessor
    preprocessor_path = base_dir / "preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_path)
    logger.info(f"Saved preprocessor to {preprocessor_path}")
    
    # 3. Define models to train
    models_to_train = [
        ("rf", RandomForestTrainer, {'n_estimators': 100, 'random_state': 42}),
        ("xgb", XGBoostTrainer, {'n_estimators': 100, 'random_state': 42}),
        ("svm", SVMTrainer, {'C': 1.0, 'probability': True, 'random_state': 42}),
        ("mlp", MLPTrainer, {'hidden_layer_sizes': (100,), 'max_iter': 500, 'random_state': 42}),
        ("logreg", LogisticRegressionTrainer, {'max_iter': 1000, 'random_state': 42})
    ]
    
    for name, trainer_class, config in models_to_train:
        logger.info(f"Training {name} model...")
        trainer = trainer_class(config)
        trainer.feature_names = feature_names
        
        # XGBoost can use validation data
        if name == "xgb":
            trainer.train(X_train, y_train, X_val=X_test, y_val=y_test)
        else:
            trainer.train(X_train, y_train)
            
        logger.info(f"Evaluating {name} model...")
        metrics = trainer.evaluate(X_test, y_test)
        logger.info(f"{name.upper()} Metrics: Accuracy={metrics['accuracy']:.4f}, F1={metrics['f1']:.4f}")
        
        # 4. Save model to subfolder
        model_name_dir = name
        if name == "xgb":
            model_name_dir = "xgboost" # Special case to match existing structure
            
        model_dir = base_dir / model_name_dir
        trainer.save(model_dir, filename=f"{name}_model.pkl")
        
        # 5. Create symlink in base_dir
        # link_name: model.joblib -> subfolder/name_model.pkl
        link_path = base_dir / f"{name}.joblib"
        # Relative target for the symlink
        target_rel_path = f"{model_name_dir}/{name}_model.pkl"
        
        # Remove old file/link if exists
        if link_path.exists() or link_path.is_symlink():
            if link_path.is_dir():
                import shutil
                shutil.rmtree(link_path)
            else:
                link_path.unlink()
            
        os.symlink(target_rel_path, link_path)
        logger.info(f"Created symlink: {link_path} -> {target_rel_path}")


if __name__ == "__main__":
    regenerate_all_models()
