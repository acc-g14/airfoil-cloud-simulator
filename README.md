# airfoil-cloud-simulator

Start celery worker:

celery -A workertasks worker --loglevel=info --concurrency=1

Start server with REST endpoints:

python server.py

Create job with arguments with:

curl -X POST 127.0.0.1:5000/job -d "n0=0&n1=0&n2=1&n3=2&min_angle=0&max_angle=90&step=45&num_nodes=200&refinement_level=0&num_samples=2&viscosity=0.0001&speed=10&time=0.1"