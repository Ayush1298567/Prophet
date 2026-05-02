import { useCallback, useRef, useState } from 'react';
import { Header } from './components/Header';
import { TriageQueue } from './components/TriageQueue';
import { PhaseProgress } from './components/PhaseProgress';
import { AgentStream } from './components/AgentStream';
import { ExploitPanel } from './components/ExploitPanel';
import { DefencePanel } from './components/DefencePanel';
import { ApprovalGate } from './components/ApprovalGate';
import { Landing } from './components/Landing';
import { PerlinHero } from './components/PerlinHero';
import { cves } from './data/cves';
import { mockEvents } from './data/mockEvents';
import type { AgentEvent, PatchDiffEvent, SigmaRuleEvent, ExploitStatusEvent } from './data/mockEvents';
import { startReplay } from './data/replayController';
import type { ReplayHandle } from './data/replayController';
import './index.css';

type Phase = 'INTEL' | 'PLAN' | 'EXECUTE' | 'DEFEND';
type ExploitStatus = 'idle' | 'running' | 'vulnerable' | 'blocked';

export default function App() {
  const [view, setView] = useState<'landing' | 'console'>('landing');
  const [isRunning, setIsRunning] = useState(false);
  const [selectedCveId, setSelectedCveId] = useState('CVE-2021-44228');
  const [currentPhase, setCurrentPhase] = useState<Phase | null>(null);
  const [completedPhases, setCompletedPhases] = useState<Phase[]>([]);
  const [streamEvents, setStreamEvents] = useState<AgentEvent[]>([]);
  const [gateOpen, setGateOpen] = useState(false);
  const [exploitStatus, setExploitStatus] = useState<ExploitStatus>('idle');
  const [exploitExcerpt, setExploitExcerpt] = useState<string | undefined>(undefined);
  const [patchDiff, setPatchDiff] = useState<string | null>(null);
  const [sigmaRule, setSigmaRule] = useState<string | null>(null);

  const replayRef = useRef<ReplayHandle | null>(null);

  const handleEvent = useCallback((event: AgentEvent) => {
    if (event.kind === 'phase') {
      setCurrentPhase(event.phase);
      setStreamEvents((prev) => [...prev, event]);
    } else if (event.kind === 'phase_complete') {
      setCompletedPhases((prev) =>
        prev.includes(event.phase) ? prev : [...prev, event.phase]
      );
      setCurrentPhase(null);
      setStreamEvents((prev) => [...prev, event]);
    } else if (event.kind === 'human_gate') {
      setGateOpen(true);
      setStreamEvents((prev) => [...prev, event]);
    } else if (event.kind === 'exploit_status') {
      const e = event as ExploitStatusEvent;
      setExploitStatus(e.status);
      if (e.responseExcerpt) setExploitExcerpt(e.responseExcerpt);
      setStreamEvents((prev) => [...prev, event]);
    } else if (event.kind === 'patch_diff') {
      setPatchDiff((event as PatchDiffEvent).content);
    } else if (event.kind === 'sigma_rule') {
      setSigmaRule((event as SigmaRuleEvent).content);
    } else {
      setStreamEvents((prev) => [...prev, event]);
    }
  }, []);

  const handleRun = () => {
    setIsRunning(true);
    setStreamEvents([]);
    setCurrentPhase(null);
    setCompletedPhases([]);
    setGateOpen(false);
    setExploitStatus('idle');
    setExploitExcerpt(undefined);
    setPatchDiff(null);
    setSigmaRule(null);

    const handle = startReplay(
      mockEvents,
      handleEvent,
      (_resolve) => {
        // Gate opened via handleEvent processing the human_gate event
      },
    );
    replayRef.current = handle;
  };

  const handleAuthorize = () => {
    setGateOpen(false);
    replayRef.current?.authorize();
  };

  const handleHold = () => {
    setGateOpen(false);
    replayRef.current?.reset();
    setIsRunning(false);
  };

  if (view === 'landing') {
    return <Landing onEnter={() => setView('console')} />;
  }

  return (
    <>
      {/*
        Global atmospheric layers — z-index 0–3.
        pointer-events: none on all, so console interactions pass through.
        Mesh at opacity 0.12, segments 64 for console performance.
      */}
      {/* segments=64 instead of 96 — cheaper on GPU while the agent stream animates */}
      <PerlinHero className="console-mesh" segments={64} />
      <div className="console-dither" aria-hidden />
      <div className="console-vignette" aria-hidden />
      <div className="console-scanlines" aria-hidden />

      {/* Console shell — z-index 5 */}
      <div className="app">
        <Header isRunning={isRunning} onRunClick={handleRun} />

        <div className="main-layout">
          <TriageQueue
            cves={cves}
            selectedId={selectedCveId}
            onSelect={setSelectedCveId}
          />

          <main className="center-column">
            <PhaseProgress
              currentPhase={currentPhase}
              completedPhases={completedPhases}
            />
            <AgentStream events={streamEvents} gateOpen={gateOpen} />
          </main>

          <aside className="right-column">
            <ExploitPanel status={exploitStatus} responseExcerpt={exploitExcerpt} />
            <DefencePanel patchDiff={patchDiff} sigmaRule={sigmaRule} />
          </aside>
        </div>

        {gateOpen && (
          <ApprovalGate onAuthorize={handleAuthorize} onHold={handleHold} />
        )}
      </div>
    </>
  );
}
