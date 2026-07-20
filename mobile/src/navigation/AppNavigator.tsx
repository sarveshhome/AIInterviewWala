import React from 'react';
import { ActivityIndicator, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useAppSelector } from '@core/store/hooks';
import { tokenStorage } from '@core/storage/mmkv';

import { LoginScreen } from '@features/auth/screens/LoginScreen';
import { RegisterScreen } from '@features/auth/screens/RegisterScreen';
import { InterviewSetupScreen } from '@features/interview/screens/InterviewSetupScreen';
import { InterviewSessionScreen } from '@features/interview/screens/InterviewSessionScreen';
import { ResumeUploadScreen } from '@features/resume/screens/ResumeUploadScreen';
import { CareerScreen } from '@features/career/screens/CareerScreen';
import { DashboardScreen } from '@features/analytics/screens/DashboardScreen';
import { DashboardTabIcon, InterviewTabIcon, ResumeTabIcon, CareerTabIcon, TAB_BRAND, TAB_MUTED } from '@shared/components/tabIcons';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const HomeTabs = () => (
  <Tab.Navigator
    screenOptions={{
      headerShown: true,
      tabBarActiveTintColor: TAB_BRAND,
      tabBarInactiveTintColor: TAB_MUTED,
    }}
  >
    <Tab.Screen
      name="Dashboard"
      component={DashboardScreen}
      options={{ title: 'Dashboard', tabBarIcon: ({ focused }) => <DashboardTabIcon focused={focused} /> }}
    />
    <Tab.Screen
      name="InterviewSetup"
      component={InterviewSetupScreen}
      options={{ title: 'Interview', tabBarIcon: ({ focused }) => <InterviewTabIcon focused={focused} /> }}
    />
    <Tab.Screen
      name="Resume"
      component={ResumeUploadScreen}
      options={{ title: 'Resume', tabBarIcon: ({ focused }) => <ResumeTabIcon focused={focused} /> }}
    />
    <Tab.Screen
      name="Career"
      component={CareerScreen}
      options={{ title: 'Career', tabBarIcon: ({ focused }) => <CareerTabIcon focused={focused} /> }}
    />
  </Tab.Navigator>
);

export const AppNavigator = () => {
  const isAuthenticated = useAppSelector((s) => s.auth.isAuthenticated);
  const hasToken = !!tokenStorage.get();

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {!isAuthenticated || !hasToken ? (
          <>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Register" component={RegisterScreen} options={{ title: 'Sign up' }} />
          </>
        ) : (
          <>
            <Stack.Screen name="Home" component={HomeTabs} options={{ headerShown: false }} />
            <Stack.Screen name="InterviewSession" component={InterviewSessionScreen} options={{ title: 'Session' }} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};