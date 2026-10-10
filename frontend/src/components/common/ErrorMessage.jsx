export default function ErrorMessage({ message }) {
  return (
    <div className="rounded-xl border border-red-500/50 bg-red-500/10 p-4 text-sm text-red-200">
      {message || 'A data error occurred.'}
    </div>
  );
}
