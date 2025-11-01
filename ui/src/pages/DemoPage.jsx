import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';

export const DemoPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-8">
      <div className="text-center space-y-8">
        <h1 className="text-5xl text-emerald-800 font-bold">Demo Page</h1>
        <p className="text-xl text-gray-300">Demo content coming soon...</p>
        <Button 
          variant="success"
          onClick={() => navigate('/')}
        >
          Back to Home
        </Button>
      </div>
    </div>
  );
};
