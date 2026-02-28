import React from 'react';
import { Clipboard, ShieldCheck, Activity } from 'lucide-react';

const MedicalDashboard = ({ data }) => {
    if (!data) return null;

    const { metadata, report, image } = data;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="space-y-6">
                <div className="bg-black rounded-lg overflow-hidden border border-gray-800 flex items-center justify-center min-h-[400px]">
                    <img src={image} alt="DICOM Scan" className="max-w-full h-auto" />
                </div>

                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <Activity className="mr-2 text-blue-500" /> Patient Metadata
                    </h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <p className="text-gray-500">Modality</p>
                            <p className="font-medium">{metadata.Modality}</p>
                        </div>
                        <div>
                            <p className="text-gray-500">Body Part</p>
                            <p className="font-medium">{metadata.BodyPartExamined}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="space-y-6">
                <div className="bg-white p-8 rounded-lg shadow-md border-t-4 border-t-blue-600">
                    <div className="flex justify-between items-start mb-6">
                        <h3 className="text-xl font-bold text-gray-800 flex items-center">
                            <Clipboard className="mr-2 text-blue-600" /> Radimal AI Insight
                        </h3>
                        {data.status === 'needs_human_review' ? (
                            <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded flex items-center font-semibold">
                                <Activity className="w-3 h-3 mr-1" /> Needs Human Review
                            </span>
                        ) : (
                            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded flex items-center font-semibold">
                                <ShieldCheck className="w-3 h-3 mr-1" /> Validated by Guardrail
                            </span>
                        )}
                    </div>

                    <div className="space-y-6">
                        <section>
                            <h4 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-2">Findings</h4>
                            <p className="text-gray-700 leading-relaxed">{report.Findings}</p>
                        </section>

                        <section className="bg-blue-50 p-4 rounded-md">
                            <h4 className="text-sm font-bold text-blue-800 uppercase tracking-wider mb-2">Impression</h4>
                            <p className="text-blue-900 font-medium">{report.Impression}</p>
                        </section>

                        <section>
                            <h4 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-2">Recommendations</h4>
                            <p className="text-gray-700">{report.Recommendations}</p>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MedicalDashboard;
