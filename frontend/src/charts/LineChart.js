import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend, Tooltip } from "recharts";
   

const LineChartComponent = ( { data } ) => {
    return (
        <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" padding={{left: 10, right: 0}} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="temperature" stroke="#5AB2FF" strokeWidth={ 3 } activeDot={{ r: 10 }} />
            </LineChart>
        </ResponsiveContainer>
    );
};

export default LineChartComponent;