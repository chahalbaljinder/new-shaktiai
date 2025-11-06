export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        <div className="mt-4 text-xl text-purple-600">Loading SHAKTI-AI...</div>
      </div>
    </div>
  )
}