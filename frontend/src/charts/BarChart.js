import React from "react";
import { BarChart, Bar, Tooltip, Legend, CartesianGrid, XAxis, YAxis, Rectangle, ResponsiveContainer } from "recharts";

const BarChartComponent = ( {data} ) => {
    return (
        <ResponsiveContainer width="50%">
            <h5>Current temperature in selected cities</h5>
            <BarChart data={data} >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name"/>
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="temperature" fill="#62c1e5" activeBar={<Rectangle stroke="#5AB2FF" />} />
            </BarChart>
        </ResponsiveContainer>
        
    );
};

export default BarChartComponent;