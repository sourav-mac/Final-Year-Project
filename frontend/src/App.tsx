import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { FiUpload, FiCheck, FiX } from 'react-icons/fi'
import { BiMoviePlay } from 'react-icons/bi'
import axios from 'axios'

interface UploadResult {
  prediction_score: number;
  filename: string;
}

function App() {
  const [result, setResult] = useState<UploadResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    const formData = new FormData()
    formData.append('video', file)

    setIsLoading(true)
    setError(null)
    
    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err) {
      setError('Failed to process video. Please try again.')
      console.error('Upload error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov']
    },
    maxFiles: 1
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-hidden">
      {/* Header */}
      <header className="relative bg-black/30 backdrop-blur-sm border-b border-white/10 py-6">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-500/10 animate-gradient"></div>
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center space-x-3">
            <BiMoviePlay className="text-4xl text-primary-400 animate-float" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 via-accent-400 to-primary-400 animate-gradient bg-clip-text text-transparent">
              Deepfake Detection System
            </h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Video Upload Section */}
          <section className="bg-black/30 backdrop-blur-sm rounded-xl p-6 border border-white/10 transition-all duration-300 hover:border-primary-500/50 hover:shadow-lg hover:shadow-primary-500/10">
            <h2 className="text-2xl font-semibold mb-6 text-primary-100">Upload Video</h2>
            
            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-8 transition-all duration-300 ${
                isDragActive
                  ? 'border-primary-400 bg-primary-400/5'
                  : 'border-gray-600 hover:border-primary-400/50'
              }`}
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center text-center space-y-4">
                <FiUpload className={`text-4xl ${
                  isDragActive ? 'text-primary-400' : 'text-gray-400'
                } animate-float`} />
                <div>
                  <p className="text-lg font-medium mb-1">
                    {isDragActive
                      ? 'Drop the video here'
                      : 'Drag & drop a video here'}
                  </p>
                  <p className="text-sm text-gray-400">
                    Supports MP4, AVI, or MOV format
                  </p>
                </div>
              </div>
            </div>

            {/* Loading State */}
            {isLoading && (
              <div className="mt-8">
                <div className="flex items-center justify-center space-x-4 p-6 bg-gray-800/50 rounded-xl backdrop-blur-sm">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-400"></div>
                  <p className="text-primary-400 font-medium">Analyzing video...</p>
                </div>
              </div>
            )}

            {/* Error State */}
            {error && (
              <div className="mt-8 p-6 bg-red-500/10 border border-red-500/20 rounded-xl backdrop-blur-sm">
                <div className="flex items-center space-x-3">
                  <FiX className="text-2xl text-red-500" />
                  <p className="text-red-400">{error}</p>
                </div>
              </div>
            )}
          </section>

          {/* Results Section */}
          {result && !isLoading && (
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/5 to-accent-500/5 rounded-xl" />
              <div className="relative p-8 bg-gray-800/50 rounded-xl backdrop-blur-sm border border-white/10 hover:border-primary-500/50 transition-all duration-300">
                <h2 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                  <FiCheck className="text-green-400 animate-float" />
                  <span className="text-primary-100">Analysis Complete</span>
                </h2>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-sm text-gray-400 mb-1">File Analyzed</p>
                    <p className="font-medium truncate text-primary-200">{result.filename}</p>
                  </div>

                  <div>
                    <p className="text-sm text-gray-400 mb-3">Prediction Score</p>
                    <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full transition-all duration-1000 ease-out animate-pulse-slow"
                        style={{
                          width: `${result.prediction_score * 100}%`,
                          background: `linear-gradient(to right, 
                            var(--primary-500), 
                            var(--accent-500)
                          )`
                        }}
                      ></div>
                    </div>
                    <div className="flex justify-between mt-2 text-sm text-gray-400">
                      <span>Real (0.0)</span>
                      <span>Fake (1.0)</span>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-white/10">
                    <div className={`p-4 rounded-lg text-center font-bold ${
                      result.prediction_score < 0.5 
                        ? 'bg-green-500/10 text-green-400 animate-glow'
                        : 'bg-red-500/10 text-red-400 animate-glow'
                    }`}>
                      {result.prediction_score < 0.5 
                        ? "✓ This video appears to be REAL" 
                        : "⚠ This video appears to be FAKE"}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
