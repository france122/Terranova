import { useParams } from 'react-router-dom';
import KnowledgeMap from '../components/Map/KnowledgeMap';
export default function ChapterMapPage() {
  const { courseId } = useParams<{ courseId: string }>();
  return <KnowledgeMap courseId={courseId || 'ds'} />;
}
