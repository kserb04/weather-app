import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const countMain = (data) => {
    const counted = data.reduce((acc, curr) => {
        if (acc[curr.main]) {
            acc[curr.main] += 1;
        } else {
            acc[curr.main] = 1;
        }
        return acc;
    }, {});

    return Object.keys(counted).map(key => ({
        name: key,
        value: counted[key]
    }));
};

const COLORS = ['#1c96c5', '#62c1e5', '#a0d9ef', '#cfecf7', '#023e8a', '#00b4d8' ]; // add more !

const PieChartComponent = ( {data} ) => {
    const countedData = countMain(data);

    return (
        <ResponsiveContainer width="30%">
            <h5>Distribution of different weather conditions in selected cities</h5>
            <PieChart height={100}>
                <Pie data={countedData} cx="50%" cy="50%" outerRadius="70%" dataKey="value" label>
                    {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend align="center" />
            </PieChart>
        </ResponsiveContainer>
    );
};

export default PieChartComponent;