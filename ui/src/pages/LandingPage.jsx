import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';

export const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[url(/map.jpg)] flex items-center justify-center p-8">
      <div className="text-center text-emerald-800 max-w-4xl font-mono">
        <p className="text-black font-oswald" style={{ fontSize: '45px' }}>
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}>G</span>eospatially
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> E</span>nhanced
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> S</span>earch
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> W</span>ith
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> T</span>errain
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> A</span>ugmented
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> L</span>ocation
          <span className="font-bold text-emerald-800 text-shadow-lg/10" style={{ fontSize: '54px' }}> T</span>argeting
        </p>
        <br /><br /><br />
        <h1 className="font-serif text-shadow-lg/30" style={{ fontSize: '108px' }}>G E S T A L T</h1>
        <br /><br /><br />
        <div className="flex flex-col gap-10 items-center box-shadow-lg/30">
          <Button
            variant="success"
            size="lg"
            onClick={() => navigate('/search')}
            style={{ padding: '0 2.5rem', boxShadow: '10px 10px 10px rgba(0, 0, 0, 0.5)' }}
          >
            Get Started
          </Button>
          <Button
            variant="success"
            size="lg"
            onClick={() => navigate('/demo')}
            style={{ padding: '0 5rem', boxShadow: '10px 10px 10px rgba(0, 0, 0, 0.5)' }}
          >
            Demo
          </Button>
        </div>
      </div>
    </div>
  );
};
