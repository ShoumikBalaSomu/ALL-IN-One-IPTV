import React from 'react';

// Note: Ensure dependencies are installed (`npm install`) 
// inside admin_panel/frontend to run this Next.js App Route.

export default function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 font-sans">
      
      {/* Header */}
      <header className="mb-8 border-b border-gray-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-blue-500">IPTV Control Center</h1>
          <p className="text-gray-400">Phase 8 Multi-Tenant Administration</p>
        </div>
        <div className="flex gap-4">
          <span className="px-3 py-1 bg-green-900 text-green-400 rounded-full text-sm">System Healthy</span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        
        {/* Telemetry Cards */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-lg">
          <h2 className="text-gray-400 text-sm uppercase tracking-widest mb-2">Active Streams</h2>
          <p className="text-4xl font-bold">1,450</p>
          <p className="text-green-500 text-sm mt-2">↑ +120 since last sync</p>
        </div>

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-lg">
          <h2 className="text-gray-400 text-sm uppercase tracking-widest mb-2">Dead Links Dropped</h2>
          <p className="text-4xl font-bold text-red-500">320</p>
          <p className="text-gray-500 text-sm mt-2">Auto-purged</p>
        </div>

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-lg">
          <h2 className="text-gray-400 text-sm uppercase tracking-widest mb-2">Last Aggregation</h2>
          <p className="text-2xl font-bold mt-2">10 Mins Ago</p>
          <button className="mt-4 w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-semibold transition-colors">
            Force Sync Now
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Token Manager */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-xl font-bold mb-4 border-b border-gray-800 pb-2">Multi-Tenant Token Manager</h2>
          <p className="text-sm text-gray-400 mb-4">Generate private M3U links restricted to specific regions.</p>
          
          <div className="flex flex-col gap-3">
            <input type="text" placeholder="Username (e.g. GuestRoomTV)" className="bg-gray-800 p-3 rounded text-white border border-gray-700 outline-none focus:border-blue-500" />
            <input type="text" placeholder="Allowed Countries (e.g. US,UK,FR)" className="bg-gray-800 p-3 rounded text-white border border-gray-700 outline-none focus:border-blue-500" />
            <button className="bg-green-600 hover:bg-green-700 py-3 rounded font-bold transition-colors">
              Generate Private Token
            </button>
          </div>
        </div>

        {/* Stream Previewer */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h2 className="text-xl font-bold mb-4 border-b border-gray-800 pb-2">WASM Stream Previewer</h2>
          <p className="text-sm text-gray-400 mb-4">Click any stream in the database to verify health locally.</p>
          
          <div className="aspect-video bg-black rounded-lg border border-gray-800 flex items-center justify-center">
            {/* Native HTML5 Video utilizing hls.js for WASM playback would mount here */}
            <p className="text-gray-600">Video Player Not Initialized</p>
          </div>
        </div>

      </div>
    </div>
  );
}
