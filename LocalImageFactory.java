package skyview.survey;

/** This class implements a cache where images
 *  may be stored after being retrieved.  This class
 *  will generate a FitsImage if the file is in the
 *  cache, or a proxy image if it is not.  The proxy
 *  will have an approximation to the WCS of the real image.
 */

import skyview.executive.Settings;

import skyview.survey.Image;
import skyview.survey.ProxyImage;

import skyview.geometry.Scaler;
import skyview.geometry.Projection;
import skyview.geometry.CoordinateSystem;
import skyview.geometry.WCS;

import java.io.File;

public class LocalImageFactory implements ImageFactory {
    
  static final public String DFT_CACHE  = "." + File.separator + "skycache" + File.separator;

  static private java.util.regex.Pattern comma = java.util.regex.Pattern.compile(",");

  public Image factory(String spell) {
    
    if (Settings.get("SpellSuffix") != null) {
        spell += Settings.get("SpellSuffix");
    }
    if (Settings.get("SpellPrefix") != null) {
        spell = Settings.get("SpellPrefix") + spell;
    }

    String[] tokens = comma.split(spell);  
    String url = tokens[0];
    System.err.println("LocalImageFactory: Opening image @ "+url);
    if (new File(url).exists()) {                    
        try {
          return new FitsImage(url);
        } catch (SurveyException s) {
          System.err.println(s);
          return null;
        }
      } else {
        System.err.println("No such file " + url);
        return null;
      }
  
  }
    
  public static String getSurveySubdir() {
    String subdir = null;
    String[]   dirs = Settings.getArray("shortname");
    if (dirs.length == 0) {
      return null;
    } else {
      subdir = dirs[0];
      subdir = subdir.replaceAll("[^a-zA-Z0-9\\-\\_\\+\\.]", "_");
    }
    return subdir;        
  }

  public static String getCachedFileName(String file) {
    String   cacheString  = Settings.get("cache", DFT_CACHE);
    String[] caches       = comma.split(cacheString);

    boolean  appendSurvey = Settings.has("SaveBySurvey");
    String   subdir       =  null;

    if (appendSurvey) {
      subdir = getSurveySubdir();
      if (subdir == null) {
        appendSurvey = false;
      }
    }

    // First try the caches without the survey
    // name appended

    for (String cache: caches) {
      String test = cache+file;
      if (new java.io.File(test).exists()) {
        return test;
      }
    }

    // Now if the user has asked for the cache to
    // be split, try inside...
    if (appendSurvey) {
      for (String cache: caches) {
        String test = cache+subdir+File.separatorChar+file;
        if (new java.io.File(test).exists()) {
          return test;
        }
      }
    }
    return null;
  }
}
