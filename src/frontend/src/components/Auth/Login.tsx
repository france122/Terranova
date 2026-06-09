import { useState, type CSSProperties, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

/* ── RPG pixel border helper ── */
const rpgBorder = (bg = '#12122a'): CSSProperties => ({
  background: bg,
  border: '3px solid #5a5a8a',
  boxShadow: 'inset 2px 2px 0 #8888bb, inset -2px -2px 0 #2a2a4a',
});

const s: Record<string, CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#0c0c1d',
    position: 'relative',
    overflow: 'hidden',
  },
  starField: {
    position: 'absolute',
    inset: 0,
    overflow: 'hidden',
  },
  card: {
    ...rpgBorder('#10102a'),
    padding: '40px 36px',
    width: 400,
    maxWidth: '90vw',
    position: 'relative',
    zIndex: 1,
  },
  swordDivider: {
    textAlign: 'center' as const,
    color: '#5a5a8a',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    letterSpacing: 4,
    marginBottom: 16,
  },
  logo: {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 20,
    textAlign: 'center' as const,
    marginBottom: 6,
    color: '#f1c40f',
    textShadow: '0 0 20px rgba(241,196,15,0.4), 2px 2px 0 #8a6a00',
    letterSpacing: 3,
    animation: 'textGlow 3s ease-in-out infinite',
  },
  subtitle: {
    textAlign: 'center' as const,
    color: '#6a6a8a',
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    marginBottom: 28,
    letterSpacing: 2,
  },
  tabs: {
    display: 'flex',
    marginBottom: 24,
    gap: 0,
  },
  tab: {
    flex: 1,
    padding: '10px 0',
    textAlign: 'center' as const,
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    border: '2px solid #5a5a8a',
    transition: 'all 0.15s',
    cursor: 'pointer',
  },
  tabActive: {
    background: 'rgba(241,196,15,0.15)',
    color: '#f1c40f',
    borderColor: '#f1c40f',
  },
  tabInactive: {
    background: 'transparent',
    color: '#6a6a8a',
    borderColor: '#2a2a4a',
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    display: 'block',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 8,
    color: '#6a6a8a',
    marginBottom: 8,
    letterSpacing: 1,
  },
  input: {
    width: '100%',
    padding: '10px 12px',
    background: '#0a0a18',
    border: '2px solid',
    borderColor: '#2a2a4a #6a6a8a #6a6a8a #2a2a4a',
    color: '#c8c8e0',
    fontFamily: "'VT323', monospace",
    fontSize: 20,
    outline: 'none',
    caretColor: '#f1c40f',
  },
  submit: {
    width: '100%',
    padding: '12px 0',
    marginTop: 12,
    background: '#5dade2',
    border: '3px solid',
    borderColor: '#8adcff #2a7aa0 #2a7aa0 #8adcff',
    color: '#0a0a18',
    fontFamily: "'Press Start 2P', monospace",
    fontSize: 10,
    letterSpacing: 1,
    cursor: 'pointer',
    transition: 'all 0.15s',
  },
  error: {
    color: '#e74c3c',
    fontFamily: "'VT323', monospace",
    fontSize: 18,
    textAlign: 'center' as const,
    marginBottom: 12,
    padding: '8px 12px',
    background: 'rgba(231,76,60,0.1)',
    border: '2px solid rgba(231,76,60,0.3)',
  },
};

/* Pixel star field - simple dots */
function StarField() {
  const stars = Array.from({ length: 60 }, (_, i) => ({
    x: ((i * 37 + 13) % 100),
    y: ((i * 53 + 7) % 100),
    size: (i % 3) + 1,
    delay: (i * 0.3) % 4,
    duration: 2 + (i % 3),
  }));

  return (
    <div style={s.starField}>
      {stars.map((star, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${star.x}%`,
            top: `${star.y}%`,
            width: star.size,
            height: star.size,
            background: i % 5 === 0 ? '#f1c40f' : i % 7 === 0 ? '#5dade2' : '#c8c8e0',
            animation: `twinkle ${star.duration}s ease-in-out ${star.delay}s infinite`,
            opacity: 0.3,
          }}
        />
      ))}
    </div>
  );
}

export default function Login() {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError('请填写用户名和密码');
      return;
    }
    setError('');
    setSubmitting(true);
    try {
      if (mode === 'login') {
        await login(username, password);
      } else {
        await register(username, password);
      }
      navigate('/map');
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || (mode === 'login' ? '用户名或密码错误' : '注册失败，请换一个用户名');
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={s.container}>
      <StarField />
      <div style={s.card}>
        <div style={s.swordDivider}>- * -</div>
        <div style={s.logo}>TERRANOVA</div>
        <div style={s.subtitle}>
          {mode === 'login' ? '- 欢迎回到新大陆 -' : '- 踏入新大陆 -'}
        </div>

        <div style={s.tabs}>
          <button
            style={{ ...s.tab, ...(mode === 'login' ? s.tabActive : s.tabInactive) }}
            onClick={() => { setMode('login'); setError(''); }}
          >
            登录
          </button>
          <button
            style={{ ...s.tab, ...(mode === 'register' ? s.tabActive : s.tabInactive) }}
            onClick={() => { setMode('register'); setError(''); }}
          >
            注册
          </button>
        </div>

        {error && <div style={s.error}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div style={s.inputGroup}>
            <label style={s.label}>EXPLORER NAME</label>
            <input
              style={s.input}
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="输入你的名字..."
              autoComplete="username"
            />
          </div>
          <div style={s.inputGroup}>
            <label style={s.label}>PASSWORD</label>
            <input
              style={s.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="输入密码..."
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            />
          </div>
          <button
            type="submit"
            style={{
              ...s.submit,
              opacity: submitting ? 0.5 : 1,
            }}
            disabled={submitting}
          >
            {submitting
              ? 'LOADING...'
              : mode === 'login'
                ? '▶ START GAME'
                : '▶ NEW GAME'}
          </button>
        </form>

        <div style={{
          ...s.swordDivider,
          marginTop: 20,
          marginBottom: 0,
        }}>- * -</div>
      </div>
    </div>
  );
}
